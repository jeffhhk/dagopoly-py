import subprocess
from .block import *

from .dagopoly import Dagopoly, DagopolyBase

class ExogenousTextBlock(Block):
    def __new__(cls, v, rfile):
        self = super().__new__(cls)
        self._v = v
        self._rfile = rfile
        return self

    def __init__(self, v, rfile):
        super().__init__()

    def sig(self):
        return compute_sig([self.__class__.__name__, self._v], [self._rfile])
    
    def get(self):
        if Dagopoly().isDebug():
            print("computing: {}".format(self.sig()))
        f = open(os.path.join(Dagopoly().adir(), "exogenous", self._rfile), "r")
        for line in f:
            yield line.rstrip("\n")
        f.close()

class ExogenousTgzTextBlock(Block):
    def __new__(cls, v, rfileTgz, rfileInside):
        self = super().__new__(cls)
        self._v = v
        self._rfile = rfileTgz
        self._rfileInside = rfileInside
        return self

    def __init__(self, v, rfileTgz, rfileInside):
        super().__init__()

    def sig(self):
        return compute_sig([self.__class__.__name__, self._v, self._rfile], [self._rfileInside])
    
    def get(self):
        if Dagopoly().isDebug():
            print("computing: {}".format(self.sig()))
        afile = os.path.join(Dagopoly().adir(), "exogenous", self._rfile)
        proc = subprocess.Popen(['tar', 'xzf', afile ,'--to-stdout', self._rfileInside],stdout=subprocess.PIPE)
        for line0 in proc.stdout:
            yield line0.decode('utf-8').rstrip()
        proc.wait()
        if proc.returncode!=0:
            raise Exception("ExogenousTgzTextBlock error status={}".format(proc.returncode))

