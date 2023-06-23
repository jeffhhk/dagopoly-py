import inspect
import hashlib
from .dagopoly import Dagopoly, DagopolyBase
import os
from types import LambdaType

import sys as _sys
from keyword import iskeyword as _iskeyword
from operator import itemgetter as _itemgetter

try:
    from _collections import _tuplegetter
except ImportError:
    _tuplegetter = lambda index, doc: property(_itemgetter(index), doc=doc)


class Block(tuple):
    def __iter__(self):
        raise TypeError("Cannot iterate Block.  Did you forget to .get()?")

def recurse_sig(arg):
    if issubclass(arg.__class__, Block):
        return arg.sig()
    if isinstance(arg, list):
        return recurse_sigs(arg)
    if isinstance(arg, tuple):
        return recurse_sigs(arg)
    if isinstance(arg, LambdaType): # Assume any functions are pure and exogenously versioned.
        return "<LambdaType>"               # Buyer beware!
    if not (isinstance(arg, int) or isinstance(arg, str)):
        print("WARNING: unexpected class {} in signature argument: {}".format(arg.__class__.__name__, arg))
    return arg

def recurse_sigs(args):
    return [recurse_sig(arg) for arg in args]

def compute_sig(tags, args):
    s = tags + recurse_sigs(args)
    # if Dagopoly().isDebug():
    #     print("sig: {}".format(s))
    return s

def hash_sig(sig):
    return hashlib.sha1(str(sig).encode('utf-8')).hexdigest()

class CachedBlock(Block):
    def __new__(cls, block):
        self = super().__new__(cls)
        self._block = block
        return self

    def sig(self):
        return self._block.sig()

    def get(self):
        s = self._block.sig()
        h = hash_sig(s)
        rfile = os.path.join("derived", h)
        if not Dagopoly().oio().exists(rfile):
            if Dagopoly().isDebug():
                print("populating: {} at {}".format(s, rfile))
            if not Dagopoly().isDryRun():
                Dagopoly().oio().write(self._block.get(), rfile)
        else:
            if Dagopoly().isDebug():
                print("remembering: {} at {}".format(s, rfile))
        if Dagopoly().isDryRun():
            return ()
        else:
            return Dagopoly().oio().read(rfile)

class CachableBlock(Block):
    def cached(self):
        return CachedBlock(self)

def block(v):
    def decorator(func):
        def _class(typename, field_names):
            typename = _sys.intern(str(typename))

            def _new(cls, *args):
                self = Block.__new__(cls)
                self._l = args
                return self

            def _get(self):
                if Dagopoly().isDebug():
                    print("computing: {}".format(self.sig()))
                args=self._l
                return func(*args)
            
            def _sig(self):
                return compute_sig([v, typename], self._l)

            def _cached(self):
                return CachedBlock(self)

            class_namespace = {
                '__doc__': f'{typename}',
                '__slots__': (),
                '_fields': field_names,
                '__new__': _new,
                'get':_get,
                'sig':_sig,
                'cached':_cached,
            }
            for index, name in enumerate(field_names):
                doc = _sys.intern(f'Alias for field number {index}')
                class_namespace[name] = _tuplegetter(index, doc)

            result = type(typename, (Block,), class_namespace)

            return result

        return _class(func.__name__, inspect.getfullargspec(func).args)
    return decorator

# same as block, but with diagnostic code removed
def block_min(v):
    def decorator(func):
        def _class(typename):
            typename = _sys.intern(str(typename))

            def _new(cls, *args):
                self = Block.__new__(cls)
                self._l = args
                return self

            def _get(self):
                args=self._l
                return func(*args)

            def _sig(self):
                return compute_sig([v, typename], self._l)

            def _cached(self):
                return CachedBlock(self)

            class_namespace = {
               '__new__': _new,
                'get':_get,
                'sig':_sig,
                'cached':_cached,
            }

            return type(typename, (Block,), class_namespace)

        return _class(func.__name__)
    return decorator
