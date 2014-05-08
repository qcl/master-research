# -*- coding: utf-8 -*-
# qcl
# Build a confusion matrix to improve the performance

import os
import sys
import simplejson as json

def confusionMatrixBuilder():
    pass

if __name__ == "__main__":
    if len(sys.argv) > 1:
        confusionMatrixBuilder()
    else:
        print "$ python ./confusionMatrix.py [R2P dir] "

