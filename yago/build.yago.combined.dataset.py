# -*- coding: utf-8 -*-
# qcl
# build the yago testing dataset's combined file from dbpedia combined file.

import os
import sys
import copy
import Queue
import multiprocessing
import simplejson as json
import pymongo
from datetime import datetime

def filterFunction(jobid,filename,inputPath,inputPtnPath,outputPath,outputPtnPath):
    contentJson = json.load(open(os.path.join(inputPath,filename),"r"))
    contentPtnJson = json.load(open(os.path.join(inputPtnPath,filename),"r"))
    print "Worker %d : Read %s into filter" % (jobid,filename)

    connect = pymongo.Connection()
    db = connect.projizz
    collection = db.result.yago.answer
    queries = map(lambda x: x[:-4], contentJson)
    itr = collection.find({"revid":{"$in":queries}})
    print "worker %d query=%d, result=%d" % (jobid,len(queries),itr.count())

    yagoJson = {}
    yagoPtn = {}
    count = 0

    for ans in itr:
        count += 1
        key = "%s.txt" % (ans["revid"])
        yagoJson[key] = contentJson[key]
        yagoPtn[key] = contentPtnJson[key]

    if count > 0:
        json.dump(yagoJson, open(os.path.join(outputPath,filename),"w"))
        json.dump(yagoPtn, open(os.path.join(outputPtnPath,filename),"w"))

    return count


def main(inputPath,inputPtnPath,outputPath,outputPtnPath):

    start_time = datetime.now()

    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count()) 
    t = 0
    result = []
    for filename in os.listdir(inputPath):
        if ".json" in filename:
            result.append(pool.apply_async(filterFunction, (t,filename,inputPath,inputPtnPath,outputPath,outputPtnPath, )))
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
    if len(sys.argv) > 4:
        inputPath = sys.argv[1]
        inputPtnPath = sys.argv[2]
        outputPath = sys.argv[3]
        outputPtnPath = sys.argv[4]
        main(inputPath,inputPtnPath,outputPath,outputPtnPath)
    else:
        print "$ python ./build.yago.combined.dataset.py [input-dir] [input-ptn-dir] [output-dir] [output-ptn-dir]"

