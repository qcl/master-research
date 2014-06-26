# -*- coding: utf-8 -*-
# qcl
# generate model from support instance

import os
import sys
import projizz
import multiprocessing
from datetime import datetime

#
#
#
def mapper(jobid, filename, inputTestPath):
    contentPtnJson = projizz.jsonRead( os.path.join(inputTestPath, filename) )
    keys = map(lambda x: x, contentPtnJson)
    print "Worker %d read %s, done." % (jobid, filename)
    return keys

#
#
#
def generate(inputSPIpath,inputTestPath,outputVSMpath,confidence):
    
    # Checking output path
    projizz.checkPath(outputVSMpath)

    model, table = projizz.readPrefixTreeModelWithTable("../yago/yagoPatternTree.model", "../patty/yagoPatternTreeWithConfidence.table")

    # Processes pool
    proceessorNumber = multiprocessing.cpu_count()
    if proceessorNumber > 20:
        proceessorNumber = 20
    pool = multiprocessing.Pool(processes=proceessorNumber)

    # Collect not used keys
    # because using 5-fold CV
    t = 0
    result = []
    for filename in os.listdir(inputTestPath):
        if ".json" in filename:
            result.append( pool.apply_async( mapper, (t,filename,inputTestPath) )  )
            t += 1
    pool.close()
    pool.join()

    notUsedKeys = []
    for r in result:
        ks = r.get()
        notUsedKeys += ks

    ### Build Model
    # Paatern Selection
    modelArticles = projizz.buildYagoProperties([])
    words = []
    count = 0
    for filename in os.listdir(inputSPIpath):
        if ".json" in filename:
            ptnId = filename[:-5]

            # ignore invalidate pattern
            if not projizz.isPatternValidate(ptnId, table, confidence=confidence):
                continue

            count += 1
            print count,ptnId

            ptnInstance = projizz.jsonRead( os.path.join(inputSPIpath,filename) )
            for rela in ptnInstance:
                for key in ptnInstance[rela]:
                    # ignore in testing data's key
                    if key in notUsedKeys:
                        continue

                    for line in ptnInstance[rela][key]:
                        modelArticles[rela].append(line)
    
            if count%100 == 0:
                print "Read",count,"files"

    for relation in modelArticles:
        print relation
        f = open(os.path.join(outputVSMpath,"%s.txt" % (relation)),"w")
        for line in modelArticles[relation]:
            f.write("%s\n" % (line) )
        f.close()

#
#
#
if __name__ == "__main__":
    if len(sys.argv) > 4:
        inputSPIpath = sys.argv[1]
        inputTestPath = sys.argv[2]
        outputVSMpath = sys.argv[3]
        confidence = float(sys.argv[4])
        generate(inputSPIpath,inputTestPath,outputVSMpath,confidence)
    else:
        print "$ python ./genModelFromSI.py [spi-all] [test-part-ptn] [output-model-dir] [confidence]"
        
