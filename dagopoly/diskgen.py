
import os
import pickle
from subprocess import Popen, PIPE

class PickleGzIter():
    def __init__(self, f, proc) -> None:
        self._proc = proc
        self._f = f
        self._unpickler = pickle.Unpickler(self._f)
        self._isOpen = True
    
    def __next__(self):
        if not self._isOpen:
            return None
        if self._f.peek(1):
            return self._unpickler.load()
        else:
            self._isOpen = False
            self._f.close()
            if self._proc is not None:
                self._proc.wait()
            raise StopIteration

# mnemonic: itbl: "Iterable"
#   Is actually a lambda of zero arguments that returns iterable in the python sense

class PickleGz():
    @classmethod
    def write(cls, itbl, rfile):
        rfileTmp=rfile+".tmp"
        if os.path.exists(rfileTmp):
            os.unlink(rfileTmp)
        f = open(rfileTmp, "wb")
        proc = Popen(["gzip", "-1"],
            stdin=PIPE, 
            bufsize=1024,
            stdout=f,
            close_fds=True
        )
        g = proc.stdin
        pickler = pickle.Pickler(g, protocol=pickle.HIGHEST_PROTOCOL)
        for x in itbl.__iter__():
            pickler.dump(x)
        g.flush()
        g.close()
        proc.wait()
        f.close()
        if os.path.exists(rfile):     # write atomically
            os.unlink(rfile)
        os.rename(rfileTmp, rfile)

    @classmethod
    def read(cls, rfile):
        return PickleGz(rfile)

    def __init__(self, rfile) -> None:
        self._rfile = rfile
    
    def __iter__(self):
        proc = Popen(["gunzip", "-c", self._rfile],
            stdout=PIPE,
            close_fds=True
            )
        return PickleGzIter(proc.stdout, proc)


