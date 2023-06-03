
import os
import sys

_adir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(_adir)

from dagopoly.micro.picklegz_io import *
from dagopoly.micro.block import *
from dagopoly.micro.exogenous import *

_adirStorage=os.path.join(_adir, "storage/autobin")
Dagopoly().setAdir(_adirStorage)
Dagopoly().setIo(PickleGzIo(debug=True))

@block("v0.0")
def count_to_n(n):
    return list(range(0,n))

@block("v0.0")
def square(xs):
    return (x*x for x in xs.get())

def count_results(xs):
    return sum((1 for _ in xs.get()))

nExpected=10
n=count_results(square(count_to_n(nExpected).cached()))
if n!=nExpected:
    raise Exception("Expected {} results but got {}".format(nExpected, n))

# print("calculated {} results".format(n))


