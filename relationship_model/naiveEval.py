# -*- coding: utf-8 -*-
# qcl
# reading the json output and query the database for answers

import os
import sys
import copy
import Queue
import simplejson as json
import pymongo
from projizzWorker import Manager
from projizzReadNGramModel import readModel

def main(modelPath,inputPath,outputFileName):
    ngram, models = readModel(modelPath)
    resultQueue = Queue.Queue(0)
    for model in models:
        models[model] = {
                "tp":0, # true - postive
                "tn":0, # true - negative
                "fp":0, # false - postivie
                "fn":0  # false - negative
                }
    connect = pymongo.Connection()
    db = connect.projizz
    ansCol = db.result.data.instance

    def workerFunction(jobObj,tid,args):
        resultJson = json.load(open(os.path.join(inputPath,jobObj),"r"))
        print "worker #%02d read file %s" % (tid,jobObj) 

        queries = map(lambda x: x[:-4], resultJson)
        itr = ansCol.find({"revid":{"$in":queries}})
        print "worker #%02d query=%d, result=%d" % (tid,len(queries),itr.count())

        partAns = copy.deepcopy(models) 

        count = 0
        for ans in itr:
            count += 1
            features = ans["features"]
            resultInstance = resultJson["%s.txt" % (ans["revid"])]
            for feature in resultInstance:
                # let threshold be 1
                for relationship in partAns:
                    true = False
                    postive = False

                    if relationship in features:
                        true = True

                    if resultInstance[feature] > 0:
                        postive = True

                    if true:
                        if postive:
                            partAns[relationship]["tp"] += 1
                        else:
                            partAns[relationship]["tn"] += 1
                    else:
                        if postive:
                            partAns[relationship]["fp"] += 1
                        else:
                            partAns[relationship]["fn"] += 1

            if count % 100 == 0:
                print "worker #%02d done %d." % (tid,count)

        resultQueue.put(partAns)

    files = Queue.Queue(0)
    for filename in os.listdir(inputPath):
        if ".json" in filename:
            files.put(filename)

    manager = Manager(4)
    manager.setJobQueue(files)
    manager.setWorkerFunction(workerFunction)
    manager.startWorking()

    print "Result Queue size", resultQueue.qsize()

    while True:
        if resultQueue.empty():
            break
        try:
            r = resultQueue.get()
            for m in r:
                models[m]["tp"] += r[m]["tp"]
                models[m]["tn"] += r[m]["tn"]
                models[m]["fp"] += r[m]["fp"]
                models[m]["fn"] += r[m]["fn"]
        except:
            break

    print "start write out to %s" % (outputFileName)
    json.dump(models,open(outputFileName,"w"))
    print "done"

if __name__ == "__main__":
    if len(sys.argv) > 3:
        modelPath = sys.argv[1] # model path
        inputPath = sys.argv[2] # result.json 's path
        outputFileName = sys.argv[3] 
        main(modelPath,inputPath,outputFileName)
    else:
        print "$ python ./naiveEval.py [model-dir] [input-dir] [output-json]"

