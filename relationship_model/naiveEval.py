# -*- coding: utf-8 -*-
# qcl
# reading the json output and query the database for answers

import os
import sys
import Queue
import simplejson as json
import pymongo
from projizzWorker import Manager
from projizzReadNGramModel import readModel

def main(modelPath,inputPath):
    ngram, models = readModel(modelPath)
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




if __name__ == "__main__":
    if len(sys.argv) > 2:
        modelPath = sys.argv[1] # model path
        inputPath = sys.argv[2] # result.json 's path
        main(modelPath,inputPath)
    else:
        print "$ python ./naiveEval.py [model-dir] [input-dir]"

