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

    # Build models for relation
    # Paatern Selection
    # TODO / FIXME 
    # CHOICE (1) Build model by pattern (2) build model by relation
    modelArticles = projizz.buildYagoProperties({})
    for filename in os.listdir(inputSPIpath):
        if ".json" in filename:
            ptnId = filename[:-5]

            # ignore invalidate pattern
            if not projizz.isPatternValidate(ptnId, table, confidence=confidence):
                continue

            ptnInstance = projizz.jsonRead( os.path.join(inputSPIpath,filename) )
            for rela in ptnInstance:
                for key in ptnInstance[rela]:
                    # ignore in testing data's key
                    if key in notUsedKeys:
                        continue

                    ptntks = table[ptnId]["pattern"].split()    # NOTE - may be need stemming
                    for line in ptnInstance[rela][key]:
                        for token in projizz.removeStopwords( projizz.getNaiveToken(line) ):
                            # TODO - stemming
                            if token in ptntks:
                                continue

                            if not token in modelArticles[rela]:
                                modelArticles[rela][token] = 0

                            # Term Freq
                            modelArticles[rela][token] += 1







    


    ## Build by Relation -> need select patterns
    



    ## TODO Build by pattern


    ### Build Model
    ### Output pattern


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
        
