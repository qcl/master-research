# -*- coding: utf-8 -*-
# qcl

import projizz
import pymongo
import os
import sys

def main(part,revid):

    # Paths (on NLG workstation)
    inputPath = "/tmp2/ccli/yago-part-%s/" % (part)
    inputPtnPath = "/tmp2/ccli/yago-ptn-part-%s/" % (part)
    spPath = "../yago/yagoPSv1/ps.%s.json" % (part)

    # connect to database
    connect = pymongo.Connection()
    db = connect.projizz
    collection = db.result.yago.answer
    itr = collection.find({"revid":revid})
    
    for ans in itr:

        targetName = ans["_id"].replace("(","").replace(")","").split("_")  # get entity name's part

        print ans["_id"],targetName
        
        # prevent second ans
        break

if __name__ == "__main__":
    if len(sys.arfv) > 2
        part = sys.argv[1]
        revid = sys.argv[2]
    else:
        print "$ python simple.viewer.py [part#] [revid]"
