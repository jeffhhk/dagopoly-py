
import os
import sys
import subprocess

_adir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(_adir)

from dagopoly.micro.basics import *
from dagopoly.micro.emit import *

_adirStorage=os.path.join(_adir, "storage/autobin")
Dagopoly().setConf(Config(
        adir=_adirStorage))

os.environ["revision_control_version"]= \
    subprocess.run(["bash", os.path.join(_adir, "contrib/gitid.sh")],
                   capture_output=True,
                   encoding="utf-8").stdout.rstrip()

# def emit_listener(msg):
#     print("dagopoly", msg)
# add_emit_listener(emit_listener)

@block("v0.0")
def count_to_n(n):
    return list(range(0,n))

@block("v0.0")
def square(xs):
    return (x*x for x in xs.get())

def count_results(xs):
    return sum((1 for _ in xs.get()))

nExpected=10
print("count_to_n={}".format(count_to_n))
print("count_to_n.get()={}".format(count_to_n(nExpected).get()))
count_to_n(nExpected)
print("about to count to n")
count_results(count_to_n(nExpected).cached())
square(count_to_n(nExpected).cached())
print("about to count squares to n")
n=count_results(square(count_to_n(nExpected).cached()).cached())
print("about to count square squares to n")
n=count_results(square(square(count_to_n(nExpected).cached()).cached()).cached())
print("about to count square square squares to n")
n=count_results(square(square(square(count_to_n(nExpected).cached()).cached()).cached()).cached())
if n!=nExpected:
    raise Exception("Expected {} results but got {}".format(nExpected, n))

print("calculated {} results".format(n))


