# -*- coding: utf-8 -*-
# qcl
# rebuild combined yago file, and split into 5 parts for 5 cv

import simplejson as json
import projizz
import os
import sys

def combined():
    files = []
    for filename in os.listdir("~/nas-3/yago/yago-json-part-a"):
        if ".json" in filename:
            files.append("~/nas-3/yago/yago-json-part-a/%s" % (filename))
    for filename in os.listdir("~/nas-3/yago/yago-json-part-b"):
        if ".json" in filename:
            files.append("~/nas-3/yago/yago-json-part-b/%s" % (filename))

    files.sort()
    print files

if __name__ == "__main__":
    combined()
