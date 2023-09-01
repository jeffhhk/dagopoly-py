
import os
import sys

_adir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(_adir)

from dagopoly.micro.basics import *
from dagopoly.micro.ipc import *

_adirStorage=os.path.join(_adir, "storage/autobin")
Dagopoly().setConf(Config(
        adir=_adirStorage))

@block("v0.0")
def count_to_n(n):
    return list(range(0,n))

@block("v0.0")
def square(xs):
    return (x*x for x in xs.get())

def count_results(xs):
    return sum((1 for _ in xs.get()))

nExpected=10
expr1 = count_to_n(nExpected)
expr2 = count_to_n(nExpected).cached()
expr3 = square(count_to_n(nExpected).cached())

run_ipc_main(sys.argv, globals(), None)


