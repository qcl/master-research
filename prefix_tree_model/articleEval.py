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

def findAnwser(jobid,filename,inputPath):
    resultJson = json.load(open(os.path.join(inputPath,filename),"r"))
    print "Worker %d : Read %s into filter" % (jobid,filename)

    connect = pymongo.Connection()
    db = connect.projizz
    collection = db.result.data.instance
    queries = map(lambda x: x[:-4], resultJson)
    itr = collection.find({"revid":{"$in":queries}})
    print "worker %d query=%d, result=%d" % (jobid,len(queries),itr.count())

    partAns = {"precision":[],"recall":[]}
    count = 0

    for ans in itr:
        count += 1
        features = ans["features"]
        resultInstance = resultJson["%s.txt" % (ans["revid"])]

        attrsFoundCount = len(resultInstance)
        correctCount = 0

        for attribute in resultInstance:
            if resultInstance[attribute] > 0:
                if attribute in features:
                    correctCount += 1
        
        precision = float(correctCount)/float(attrsFoundCount)
        recall    = float(correctCount)/float(len(features))

        partAns["precision"].append(precision)
        partAns["recall"].append(recall)

        if count % 100 == 0:
            print "worker #%d done %d." % (jobid,count)

    avgp = sum(partAns["precision"])/len(partAns["precision"])
    avgr = sum(partAns["recall"])/len(partAns["recall"])
    print "worker #%d done, avg precision = %.2f, recall = %.2f." % (jobid,avgp,avgr)

    return partAns


def main(inputPath,outputFileName):
    
    #properties = buildProperties("../naive_model/PbR/")

    start_time = datetime.now()

    result = []
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count()) 
    t = 0
    for filename in os.listdir(inputPath):
        if ".json" in filename:
            partAns = copy.deepcopy(properties)
            result.append(pool.apply_async(findAnwser, (t,filename,inputPath, )))
            t += 1
    pool.close()
    pool.join()

    anwser = {"precision":[],"recall":[]}

    for res in result:
        r = res.get()
        anwser["precision"] += r["precision"]
        anwser["recall"] += r["recall"]

    avgp = sum(anwser["precision"])/len(anwser["precision"])
    avgr = sum(anwser["recall"])/len(anwser["recall"])

    output = {"precision":avgp,"recall":avgr,"result":anwser}

    print "start write out to %s" % (outputFileName)
    json.dump(output,open(outputFileName,"w"))
    print "Precision = %f\nRecall = %f" % (avgp,avgr)

    diff = datetime.now() - start_time
    print "Spend %d.%d seconds" % (diff.seconds, diff.microseconds)

if __name__ == "__main__":
    if len(sys.argv) > 2:
        inputPath = sys.argv[1] # result.json 's path
        outputFileName = sys.argv[2] 
        main(inputPath,outputFileName)
    else:
        print "$ python ./articleEval.py [input-dir] [output-json]"

