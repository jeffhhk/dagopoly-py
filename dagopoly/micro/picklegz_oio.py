import os
from .picklegz import PickleGz
from .dagopoly import Dagopoly

class PickleGzOio():
    def __init__(self) -> None:
        pass

    def _adir(self):
        return Dagopoly().conf.adir

    def exists(self, rfile):
        return os.path.exists(os.path.join(self._adir(), rfile))

    def read(self, rfile):
        return PickleGz.read(os.path.join(self._adir(), rfile))

    def write(self, itbl, rfile):
        adir = os.path.join(self._adir(), rfile)
        adirParent = os.path.dirname(adir)
        if not os.path.exists(adirParent):
            os.makedirs(adirParent)
        PickleGz.write(itbl, adir)


