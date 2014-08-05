# -*- coding: utf-8 -*-
# qcl
# extract result from .npr, split by each variable

import os
import sys

def extract(reliability,confidence,nbc):
    if confidence <= 0.0:
        subdirname = "ptn-0"
    elif confidence <= 0.7:
        subdirname = "ptn-70"
    elif confidence <= 0.8:
        subdirname = "ptn-80"
    else:
        subdirname = "ptn-90"

    if nbc:
        dirname = "./naive-bayes/"
        nbc = 1
    else:
        nbc = 0
        if reliability <= 0.0:
            dirname = "./origin-method/"
        elif reliability <= 0.3:
            dirname = "./origin-with-ptn-threshold-0.3/"
        else:
            dirname = "./origin-with-ptn-threshold-0.5/"

    path = os.path.join(dirname,subdirname)
    if not os.path.exists(path):
        return
    #else:
    #    print path

    print "Confidence\tReliability\tNBC\tDegree\tStrategy\tTyped\tPrecision\tRecall\tMirP\tMirR"

    for filename in os.listdir(path):
        if ".npr" in filename:
            args = filename.split(".")[0].split("-")
            degree = args[0]
            strategy = args[1]
            typed = args[2]
            #print confidence,reliability,nbc,degree,strategy,typed
            f = open(os.path.join(path,filename),"r")
            for line in f:
                if "Average" in line:
                    data = line.split()
                    print "%f\t%f\t%d\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % (confidence,reliability,nbc,degree,strategy,typed,data[1],data[2],data[3],data[4])

for reliability in [0,0.3,0.5]:
    for confidence in [0,0.7,0.8,0.9]:
        extract(reliability,confidence,False)

for confidence in [0,0.7,0.8,0.9]:
    extract(0.0,confidence,True)
