# -*- coding: utf-8 -*-
# qcl
# 2014.06.05
# Remove non mentioned properties form answer set.

import os
import sys
import projizz
import multiprocessing
import simplejson as json
from datetime import datetime
from pymongo import Connection

def updateAnswer(jobid,inputPath,filename):
    contenJson = projizz.jsonRead(os.path.join(inputPath,filename))
    print "#%d - %s" % (jobid,filename)
    connect = Connection()
    answerCollection = connect.projizz.result.yago.answer
    factCollection = connect.projizz.yago.facts

    queries = map(lambda x: x[:-4], contenJson)

    itr = answerCollection.find({"revid":{"$in":queries}})
    print "#%d - query=%d,result=%d" % (jobid,len(queries),itr.count())




def main(inputPath,inputPtnPath,outputPath,outputPtnPath):

    debug = True

    if !os.path.isdir(outputPath):
        os.mkdir(outputPath)
    if !os.path.isdir(outputPtnPath):
        os.mkdir(outputPtnPath)

    result = []

    # Update answer
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
    t = 0
    for filename in os.listdir(inputPath):
        if ".json" in filename:
            if debug:
                result.append(updateAnswer(t,inputPath,filename))
            else:
                result.append(pool.apply_async(updateAnswer, (t,inputPath,filename)))

    # Rebuild articles and patterns


if __name__ == "__main__":
    if len(sys.argv) > 4:
        inputPath = sys.argv[1]
        inputPtnPath = sys.argv[2]
        outputPath = sys.argv[3]
        outputPtnPath = sys.argv[4]
        main(inputPath,inputPtnPath,outputPath,outputPtnPath)
    else:
        print "$ python ./update.rmNoMention.result.yago.answer.py inputPath inputPtnPath outputPath outputPtnPath"
