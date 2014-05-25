# -*- coding: utf-8 -*-
# qcl
# do some statistics on pattern and relation

import os
import sys
import projizz
import multiprocessing
import simplejson as json
import pymongo
from datetime import datetime

def filterFunction(jobid,filename,inputPtnPath,model,table):
    contentPtnJson = json.load(open(os.path.join(inputPtnPath,filename),"r"))
    print "Worker %d : Read %s into filter" % (jobid,filename)

    connect = pymongo.Connection()
    db = connect.projizz
    collection = db.result.yago.answer
    queries = map(lambda x: x[:-4], contentPtnJson)
    itr = collection.find({"revid":{"$in":queries}})
    print "worker %d query=%d, result=%d" % (jobid,len(queries),itr.count())

    patterns = {}

    count = 0

    for ans in itr:
        count += 1
        key = "%s.txt" % (ans["revid"])

        # Now only consider properties, no references.
        relation = ans["properties"]
        
        ptnEx = contentPtnJson[key]
        for line in ptnEx:
            for ptn in line[1]:
                ptnId = "%d" % (ptn[0])
                if not ptnId in patterns:
                    # TODO
                    patterns[ptnId] = {}




def main(inputPtnPath,outputPath):
    
    start_time = datetime.now()

    model, table = projizz.readPrefixTreeModelWithTable("./yagoPatternTree.model","./yagoPatternTree.table")

    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count()) 
    t = 0
    result = []
    for filename in os.listdir(inputPath):
        if ".json" in filename:
            result.append(pool.apply_async(filterFunction, (t,filename,inputPtnPath,model,table, )))
            t += 1
    pool.close()
    pool.join()

    count = 0
    for res in result:
        r = res.get()
        count += r

    diff = datetime.now() - start_time
    print "Spend %d.%d seconds, there are %d articles" % (diff.seconds, diff.microseconds,count)

if __name__ == "__main__":
    if len(sys.argv) > 2:
        inputPtnPath = sys.argv[1]
        outputPath = sys.argv[2]
        main(inputPtnPath,outputPath)
    else:
        print "$ python ./yago.pattern.statistics.py [input-ptn-dir] [output-filename.json]"

