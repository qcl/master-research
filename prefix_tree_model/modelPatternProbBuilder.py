# -*- coding: utf-8 -*-
# qcl
# Let the pattern in tree model only can choice 1 property. (Accroding the frequence.)

import os
import sys
import copy
import multiprocessing
import simplejson as json
import pymongo
from projizzTreeModel import readModel
from datetime import datetime

def buildProperties(path):
    properties = {}
    for filename in os.listdir(path):
        if ".txt" in filename:
            properties[filename[:-4]] = 0   # property's count
    return properties

def findAnwser(jobid,filename,inputPath,partAns):
    resultJson = json.load(open(os.path.join(inputPath,filename),"r"))
    print "Worker %d : Read %s into filter" % (jobid,filename)

    connect = pymongo.Connection()
    db = connect.projizz
    collection = db.result.data.instance
    queries = map(lambda x: x[:-4], resultJson)
    itr = collection.find({"revid":{"$in":queries}})
    print "worker %d query=%d, result=%d" % (jobid,len(queries),itr.count())


    count = 0

    for ans in itr:
        count += 1
        features = ans["features"]

        for feature in features:
            partAns[feature] += 1

        if count % 100 == 0:
            print "worker #%d done %d." % (jobid,count)

    return partAns


def main(inputModel,inputPath,outputFileName):
    
    properties = buildProperties("../naive_model/PbR/")
    treeModel = readModel(inputModel)

    start_time = datetime.now()

    result = []
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count()) 
    t = 0
    for filename in os.listdir(inputPath):
        if ".json" in filename:
            partAns = copy.deepcopy(properties)
            result.append(pool.apply_async(findAnwser, (t,filename,inputPath,partAns, )))
            t += 1
    pool.close()
    pool.join()

    for res in result:
        r = res.get()
        for m in r:
            properties[m] += r[m]
    
    # TODO - modify the tree model


    print "start write out to %s" % (outputFileName)
    json.dump(properties,open(outputFileName,"w"))

    diff = datetime.now() - start_time
    print "Spend %d.%d seconds" % (diff.seconds, diff.microseconds)

if __name__ == "__main__":
    if len(sys.argv) > 3:
        inputModel = sys.argv[1]
        inputPath = sys.argv[2] # result.json 's path
        outputFileName = sys.argv[3] 
        main(inputModel,inputPath,outputFileName)
    else:
        print "$ python ./modelPatternProbBuilder.py [input-model] [input-dir] [output-model]"

