# -*- coding: utf-8 -*-
# qcl
# Read n-gram model from dir

import os
import simplejson as json
import pickle

def toStringForm(ple):
    l = len(ple)
    s = ple[0]
    for i in xrange(1,l):
        s += "\t%s" % (ple[i])
    return s

def readModel(path):
    models = {}
    n = 1
    for modelFilename in os.listdir(path):
        if ".pkl" in modelFilename:
            f = open(os.path.join(path,modelFilename),"r")
            m = pickle.load(f)
            f.close()

            modelName = modelFilename.split(".")[0]
            models[modelName] = {}
            
            for gram in m:
                n = len(gram)
                models[modelName][toStringForm(gram)] = m[gram]

        elif ".json" in modelFilename:
            pass
            # todo

    return n,models


if __name__ == "__main__":
    n,models = readModel("./2-gramModel/")
    print n,models
