# -*- coding: utf-8 -*-
# qcl
# calculate micro & macro precision and recall for the output of experiments

import os
import sys

import simplejson as json

def calculate(filesPath):
  
    files = []
    if os.path.isdir(filesPath):
        for filename in os.listdir(filesPath):
            if ".out" in filename:
                files.append(os.path.join(filesPath,filename))
    else:
        files = [filesPath]

    result = {}

    for filename in files:
        f = open(filename,"r")
        outputResult = json.load(f)
        f.close()

        for attribute in outputResult:
            if attribute == "produced":
                continue

            if attribute not in result:
                result[attribute] = {"tp":[],"fp":[],"fn":[]}

            result[attribute]["tp"].append(len(outputResult[attribute]["tp"]))
            result[attribute]["fp"].append(len(outputResult[attribute]["fp"]))
            result[attribute]["fn"].append(len(outputResult[attribute]["fn"]))

    gTP = 0
    gFP = 0
    gFN = 0
    Precision = []
    Recall    = []

    macroByAttribute = {}
    microByAttribute = {}


    for attribute in result:
        if not attribute in macroByAttribute:
            macroByAttribute[attribute] = {"precision":0,"recall":0}
            microByAttribute[attribute] = {"precision":0,"recall":0,"tp":0,"fp":0,"fn":0}

        number = len(result[attribute]["tp"])

        precision = []
        recall = []

        tp = sum(result[attribute]["tp"])
        fp = sum(result[attribute]["fp"])
        fn = sum(result[attribute]["fn"])

        gTP += tp
        gFP += fp
        gFN += fn

        for i in range(0,number):
            _tp = result[attribute]["tp"][i]
            _fp = result[attribute]["fp"][i]
            _fn = result[attribute]["fn"][i]

            _p = 0.0
            _r = 0.0

            if float(_tp+_fp) > 0.0:
                _p = float(_tp)/float(_tp+_fp)

            if float(_tp+_fn) > 0.0:
                _r = float(_tp)/float(_tp+_fn)

            precision.append(_p)
            recall.append(_r)

        macroByAttribute[attribute]["precision"] = sum(precision)/float(len(precision))
        macroByAttribute[attribute]["recall"]    = sum(recall)   /float(len(recall))

        Precision.append(macroByAttribute[attribute]["precision"])
        Recall.append(macroByAttribute[attribute]["recall"])

        _p = 0.0
        _r = 0.0

        if float(tp+fp) > 0.0:
            _p = float(tp)/float(tp+fp)

        if float(tp+fn) > 0.0:
            _r = float(tp)/float(tp+fn)

        microByAttribute[attribute]["precision"] = _p
        microByAttribute[attribute]["recall"]    = _r
        microByAttribute[attribute]["tp"] = tp
        microByAttribute[attribute]["fp"] = fp
        microByAttribute[attribute]["fn"] = fn

    P = sum(Precision)/float(len(Precision))
    R = sum(Recall)/float(len(Recall))

    mP = 0.0
    mR = 0.0

    if float(gTP + gFP) > 0.0:
        mP = float(gTP) / float(gTP + gFP)

    if float(gTP + gFN) > 0.0:
        mR = float(gTP) / float(gTP + gFN)

    for attribute in macroByAttribute:
        print "%s\t%.08f\t%.08f\t%.08f\t%.08f\t%d\t%d\t%d" % (attribute,macroByAttribute[attribute]["precision"],macroByAttribute[attribute]["recall"],microByAttribute[attribute]["precision"],microByAttribute[attribute]["recall"],microByAttribute[attribute]["tp"],microByAttribute[attribute]["fp"],microByAttribute[attribute]["fn"])
 
    print "%s\t%.08f\t%.08f\t%.08f\t%.08f\t%d\t%d\t%d" % ("Average",P,R,mP,mR,gTP,gFP,gFN)



if __name__ == "__main__":
    if len(sys.argv) > 1:
        filesPath = sys.argv[1]
        calculate(filesPath)
    else:
        print "$ python ./calPRF.py [.out file or path contain .out files]"

