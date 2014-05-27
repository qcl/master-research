# -*- coding: utf-8 -*-
# qcl
# 

import os
import sys
import projizz
import simplejson as json

def buildModel(inputPtnPath, outputPath):
    if not os.path.isdir(outputPath):
        os.mkdir(outputPath)

    statisticFiles = []
    for filename in os.listdir(inputPtnPath):
        if ".json" in filename:
            statisticFiles.append(filename)
    statisticFiles.sort()

    for filename in statisticFiles:
        properties = projizz.buildYagoProperties({})
        for anotherFilename in statisticFiles:
            if filename == anotherFilename:
                continue
            p = json.load(open(os.path.join(inputPtnPath,anotherFilename),"r"))
            for rela in p:
                for ptnId in p[rela]:
                    if not ptnId in properties[rela]:
                        properties[rela][ptnId] = {"total":0,"support":0}
                    properties[rela][ptnId]["total"] += p[rela][ptnId]["total"]
                    properties[rela][ptnId]["support"] += p[rela][ptnId]["support"]
            
        #for relation in properties:
        #    ptns = properties[relation]
        #    print ptns.items()

        print filename
        json.dump(properties,open(os.path.join(outputPath,filename),"w"))


if __name__ == "__main__":
    if len(sys.argv) > 2:
        inputPtnPath = sys.argv[1]
        outputPath   = sys.argv[2]
        buildModel(inputPtnPath, outputPath)
    else:
        print "$ python ./yago.precision.first.model.py [inputStatisticDir] [outputDir]"
