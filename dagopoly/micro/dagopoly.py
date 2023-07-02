from .singleton import Singleton

class DagopolyBase(object):
    def __init__(self) -> None:
        self._conf = None

    @property
    def conf(self):
        if self._conf is None:
            raise Exception("setting a configuration is required")
        return self._conf

    def setConf(self,conf):
        if self._conf is None:
            self._conf = conf
        else:
            raise Exception("configuration is already set")


class Dagopoly(DagopolyBase, metaclass=Singleton):
    pass

