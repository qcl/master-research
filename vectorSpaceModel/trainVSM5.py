# -*- coding: utf-8 -*-
# qcl
# Build VSM models to decide relation, at the same time, calculate the pattern's precision =p

import sys
import projizz

def train(inputPath,inputPtnPath,outputPath):
    
    projizz.checkPath(outputPath)



if __name__ == "__main__":
    if len(sys.argv) > 3:
        # args
        inputPath = sys.argv[1]
        inputPtnPath = sys.argv[2]
        outputPath = sys.argv[3]
        train(inputPath,inputPtnPath,outputPath)
    else:
        print "$ ./trainVSM5.py [input-train-article-dir] [input-train-ptn-dir] [output-models-dir]"
