from .singleton import Singleton

class DagopolyBase(object):
    def __init__(self) -> None:
        self._adir = None
        self._io = None
        self._isDebug = None

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

    def isDebug(self):
        return self._isDebug

    def setIsDebug(self, x):
        if self._isDebug is None:
            self._isDebug = x
        else:
            raise Exception("isDebug() is already configured")

class Dagopoly(DagopolyBase, metaclass=Singleton):
    pass

