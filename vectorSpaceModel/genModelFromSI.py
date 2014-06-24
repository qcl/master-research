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
def generate(inputSPIpath,inputTestPath,outputVSMpath):

    # Processes pool
    proceessorNumber = multiprocessing.cpu_count()
    if proceessorNumber > 20:
        proceessorNumber = 20
    pool = multiprocessing.Pool(processes=proceessorNumber)

    # Collect not used keys
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

    print "not used:",notUsedKeys
    print len(notUsedKeys)

#
#
#
if __name__ == "__main__":
    if len(sys.argv) > 3:
        inputSPIpath = sys.argv[1]
        inputTestPath = sys.argv[2]
        outputVSMpath = sys.argv[3]
        generate(inputSPIpath,inputTestPath,outputVSMpath)
    else:
        print "$ python ./genModelFromSI.py [spi-all] [test-part-ptn] [output-model-dir]"
        
