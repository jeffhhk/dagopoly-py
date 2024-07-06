import os
import json
from datetime import datetime, timezone
import time
from .dagopoly import Dagopoly

def manifest_retrieve(oio, h):
    rfile = os.path.join("derived", h)
    rfileM = "{}.manifest".format(rfile)
    if not oio.exists(rfileM):
        raise Exception("This code should not run.  Bug?  The cache should test should have failed without a signature at {}".format(rfileM))
    mnfst = oio.read(rfileM, reader=Ndjson.read)
    mnfst = mnfst[0] if len(mnfst)>0 else None
    # strangely, we do not need to recurse, because we recursed before writing the manifest
    return mnfst

def manifest(sig, sighash, remembered):
    t = datetime.fromtimestamp(time.time(), tz=timezone.utc).isoformat()
    rcv = os.getenv("revision_control_version")
    oio = Dagopoly().oio
    return [{
        "revision_control_version":rcv,
        "t":t,
        "sighash": sighash,
        "sig": sig,
        "remembered": [manifest_retrieve(oio, h) for (s,h) in remembered]
    }]

class Ndjson():
    @classmethod
    def write(cls, itbl, afile):
        afileTmp=afile+".tmp"
        if os.path.exists(afileTmp):
            os.unlink(afileTmp)
        f = open(afileTmp, "w")
        for x in itbl.__iter__():
            json.dump(x,f)
            f.write("\n")
        f.close()
        if os.path.exists(afile):     # write atomically
            os.unlink(afile)
        os.rename(afileTmp, afile)

    @classmethod
    def read(cls, rfile):
        with open(rfile, "r") as f:
            return [json.load(f)]     # a list so that it is generator-compatible
