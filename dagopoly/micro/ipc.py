import os
import sys
import re
import json
from .dagopoly import Dagopoly
from .config import Config

re_safe = re.compile("([a-zA-Z0-9_-]+)")
def is_safe(symbolid):
    return re_safe.match(symbolid)
re_scrub = re.compile("\x00\x0a")
def scrub_get(x):
    return re_scrub.sub("", str(x))

""" Returns true if a command was interpreted, even if it was an error. """
def run_ipc_main(argv, globals0, locals0):
    if len(argv) <= 1:
        return False
    cmd = argv[1]
    if cmd == "sig":
        symbolid = argv[2]
        if is_safe(symbolid):
            sig = eval("{}.sig()".format(symbolid), globals0, locals0)
            jnsig = json.dumps(sig)
            print(jnsig, file=sys.stdout)
    elif cmd == "get":
        symbolid = argv[2]
        if is_safe(symbolid):
            xs = eval("{}.get()".format(symbolid), globals0, locals0)
            for x in xs:
                x = scrub_get(x)
                print(x, file=sys.stdout)
    else:
        print("unknown command: {}".format(cmd), file=sys.stderr)
    return True

