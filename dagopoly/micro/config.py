from .local_oio import LocalOio

class Config():
    def __init__(self,
                 adir=None,
                 oio=LocalOio(),
                 isDebug=False,
                 isDryRun=False
                 ):
        self._adir = adir
        self._oio = oio
        self._isDebug = isDebug
        self._isDryRun = isDryRun
    @property
    def adir(self):
        return self._adir
    """mnemonic: ObjectIO"""
    @property
    def oio(self):
        return self._oio
    # @property
    # def isDebug(self):
    #     return self._isDebug
    @property
    def isDryRun(self):
        return self._isDryRun
