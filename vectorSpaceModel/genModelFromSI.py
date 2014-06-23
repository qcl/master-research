# -*- coding: utf-8 -*-
# qcl
# generate model from support instance

import os
import sys
import projizz

#
#
#
def mapper():
    pass

#
#
#
def generate(inputSPIpath,inputTestPath,outputVSMpath):
    pass

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
        
