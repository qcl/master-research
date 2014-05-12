# -*- coding: utf-8 -*-
# qcl
# reading the json output and query the database for answers

import os
import sys
import copy
import Queue
import multiprocessing
import simplejson as json
import pymongo
from projizzTreeModel import readModel
from datetime import datetime

def buildProperties(path):
    properties = {}
    for filename in os.listdir(path):
        if ".txt" in filename:
            properties[filename[:-4]] = {
                "tp":[], # true - postive            Real Ans: True    False
                "tn":[], # true - negative    Model told:
                "fp":[], # false - postive                 Yes  tp      fp     
                "fn":[]  # false - negative                 No  fn      tn
                }
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
        resultInstance = resultJson["%s.txt" % (ans["revid"])]

        for attribute in partAns:
            postive = False
            true = False

            if attribute in resultInstance and resultInstance[attribute] > 0:
                postive = True

            if attribute in features:
                true = True

            if true:
                if postive:
                    partAns[attribute]["tp"].append(ans["revid"])
                else:
                    partAns[attribute]["fn"].append(ans["revid"])
            else:
                if postive:
                    partAns[attribute]["fp"].append(ans["revid"])
                else:
                    partAns[attribute]["tn"].append(ans["revid"])

        if count % 100 == 0:
            print "worker #%d done %d." % (jobid,count)

    return partAns


def main(inputPath,outputFileName):
    
    properties = buildProperties("../naive_model/PbR/")
    

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
            properties[m]["tp"] += r[m]["tp"]
            properties[m]["tn"] += r[m]["tn"]
            properties[m]["fp"] += r[m]["fp"]
            properties[m]["fn"] += r[m]["fn"]

    print "start write out to %s" % (outputFileName)
    json.dump(properties,open(outputFileName,"w"))

    diff = datetime.now() - start_time
    print "Spend %d.%d seconds" % (diff.seconds, diff.microseconds)

if __name__ == "__main__":
    if len(sys.argv) > 2:
        inputPath = sys.argv[1] # result.json 's path
        outputFileName = sys.argv[2] 
        main(inputPath,outputFileName)
    else:
        print "$ python ./treeEval.py [input-dir] [output-json]"

