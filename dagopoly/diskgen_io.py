import os
from dagopoly.diskgen import Diskgen
from dagopoly.singleton import Singleton

class DiskGenIo():
    def __init__(self, debug=False) -> None:
        self._debug = debug

    def _adir(self):
        return Dagopoly().adir()

    def exists(self, rfile):
        return os.path.exists(os.path.join(self._adir(), rfile))

    def read(self, rfile):
        return Diskgen.read(os.path.join(self._adir(), rfile))

    def write(self, itbl, rfile):
        adirParent = os.path.dirname(os.path.join(self._adir(), rfile))
        if not os.path.exists(adirParent):
            os.makedirs(adirParent)
        Diskgen.write(itbl, os.path.join(self._adir(), rfile))

    def isDebug(self):
        return self._debug

class DagopolyBase(object):
    def __init__(self) -> None:
        self._adir = None
        self._io = None

    def adir(self):
        if self._adir is None:
            raise Exception("adir() must be configured")
        return self._adir

    def setAdir(self,adir):
        if self._adir is None:
            self._adir = adir
        else:
            raise Exception("adir() is already configured")

    def io(self):
        return self._io

    def setIo(self, io):
        if self._io is None:
            self._io = io
        else:
            raise Exception("io() is already configured")

class Dagopoly(DagopolyBase, metaclass=Singleton):
    pass

