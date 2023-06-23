from .singleton import Singleton

class DagopolyBase(object):
    def __init__(self) -> None:
        self._adir = None
        self._oio = None
        self._isDebug = None
        self._dryRun = None

    def adir(self):
        if self._adir is None:
            raise Exception("adir() must be configured")
        return self._adir

    def setAdir(self,adir):
        if self._adir is None:
            self._adir = adir
        else:
            raise Exception("adir() is already configured")

    # mnemonic: ObjectIO
    def oio(self):
        return self._oio

    def setOio(self, oio):
        if self._oio is None:
            self._oio = oio
        else:
            raise Exception("oio() is already configured")

    def isDebug(self):
        return self._isDebug

    def setIsDebug(self, x):
        if self._isDebug is None:
            self._isDebug = x
        else:
            raise Exception("isDebug() is already configured")

    def isDryRun(self):
        return self._dryRun if self._dryRun is not None else False

    def setIsDryRun(self, dryRun):
        if self._dryRun is None:
            self._dryRun = dryRun
        else:
            raise Exception("dryRun() is already configured")


class Dagopoly(DagopolyBase, metaclass=Singleton):
    pass

