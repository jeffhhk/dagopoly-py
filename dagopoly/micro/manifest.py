import os
import json
from datetime import datetime, timezone
import time

def manifest(sig,sighash):
    t = datetime.fromtimestamp(time.time(), tz=timezone.utc).isoformat()
    rcv = os.getenv("revision_control_version")
    return [{
        "revision_control_version":rcv,
        "t":t,
        "sighash": sighash,
        "sig": sig
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
