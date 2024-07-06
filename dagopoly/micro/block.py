import inspect
import hashlib
from .dagopoly import Dagopoly, DagopolyBase
from .manifest import Ndjson, manifest
from .emit import emit
from .sigc import Sigc
import os
from types import LambdaType

import sys as _sys
from keyword import iskeyword as _iskeyword
from operator import itemgetter as _itemgetter

try:
    from _collections import _tuplegetter
except ImportError:
    _tuplegetter = lambda index, doc: property(_itemgetter(index), doc=doc)


class Block(object):
    def __iter__(self):
        raise TypeError("Cannot iterate Block.  Did you forget to .get()?")

def recurse_sig(arg):
    if issubclass(arg.__class__, Block):
        return arg.sig()
    if isinstance(arg, list) or isinstance(arg, tuple):
        return recurse_sigs(arg)
    if isinstance(arg, LambdaType): # Assume any functions are pure and exogenously versioned.
        return "<Lambda>"               # Buyer beware!
    if not (isinstance(arg, int) or isinstance(arg, str)):
        emit(["warn", "msg", "", "unexpected class {} in signature argument: {}".format(arg.__class__.__name__, arg)])
    return arg

def recurse_sigs(args):
    return [recurse_sig(arg) for arg in args]

def compute_sig(tags, args):
    s = tags + recurse_sigs(args)
    #emit(["trace", "compute_sig", "", s])
    return s

def hash_sig(sig):
    return hashlib.sha1(str(sig).encode('utf-8')).hexdigest()

class CachedBlock(Block):
    def __init__(self, block):
        self._block = block

    def sig(self):
        return self._block.sig()

    def get(self):
        s = self._block.sig()
        h = hash_sig(s)
        rfile = os.path.join("derived", h)
        rfileM = "{}.manifest".format(rfile)
        oio = Dagopoly().oio
        if not oio.exists(rfile) or not oio.exists(rfileM):
            emit(["info", "populating", s, rfile])
            sigc = Sigc()
            with sigc:
                if not Dagopoly().conf.isDryRun:
                    oio.write(self._block.get(), rfile)
            if not Dagopoly().conf.isDryRun:
                oio.write(manifest(s, h, sigc.get()),
                    rfileM, writer=Ndjson.write)
        else:
            emit(["info", "remembering", s, rfile])
            Sigc.send((s,h))
        if Dagopoly().conf.isDryRun:
            return ()
        else:
            return oio.read(rfile)

class CachableBlock(Block):
    def cached(self):
        return CachedBlock(self)

def block(v):
    def decorator(func):
        def _class(typename, field_names):
            typename = _sys.intern(str(typename))

            def _init(self, *args):
                self._l = args

            def _get(self):
                emit(["info", "computing", self.sig()])
                args=self._l
                return func(*args)
            
            def _sig(self):
                return compute_sig([v, typename], self._l)

            class_namespace = {
                '__doc__': f'{typename}',
                '__slots__': (),
                '_fields': field_names,
                '__init__': _init,
                'get':_get,
                'sig':_sig
            }
            for index, name in enumerate(field_names):
                doc = _sys.intern(f'Alias for field number {index}')
                class_namespace[name] = _tuplegetter(index, doc)

            result = type(typename, (CachableBlock,), class_namespace)

            return result

        return _class(func.__name__, inspect.getfullargspec(func).args)
    return decorator

# same as block, but with diagnostic code removed
def block_min(v):
    def decorator(func):
        def _class(typename):
            typename = _sys.intern(str(typename))

            def _get(self):
                args=self._l
                return func(*args)

            def _sig(self):
                return compute_sig([v, typename], self._l)

            class_namespace = {
                'get':_get,
                'sig':_sig
            }

            return type(typename, (CachableBlock,), class_namespace)

        return _class(func.__name__)
    return decorator
