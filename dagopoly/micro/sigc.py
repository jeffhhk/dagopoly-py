

_the_sigc = []

# Mnemonic: SIGnature Connector
class Sigc:
    def __init__(self):
        self._xs = []

    def __enter__(self):
        _the_sigc.append(self)

    def __exit__(self, exc_type, exc_value, traceback):
        _the_sigc.pop()
        #TODO? f exc_type is not None:

    def add(self,x):
        self._xs.append(x)

    def get(self):
        return self._xs

    @classmethod
    def send(cls, x):
        if len(_the_sigc) == 0:
            return
        coll = _the_sigc[-1]
        coll.add(x)

