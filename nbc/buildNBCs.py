# -*- coding: utf-8 -*-
# qcl
# build naive bayes models from dir

import os
import sys
import projizz

def buildModels(inputpath,outputPath):

    projizz.checkPath(outputPath)

    relations = projizz.getYagoRelation()
    for relation in relations:
        if relation == "produced":
            continue

        posInstances = projizz.jsonRead( os.path.join(inputpath,"%s.pos" % (relation)) )
        negInstances = projizz.jsonRead( os.path.join(inputpath,"%s.neg" % (relation)) )

        instances = []
        for data in posInstances:
            instances.append( (data["text"], data["label"]) )
        for data in negInstances:
            instances.append( (data["text"], data["label"]) )

        classifier = projizz.NaiveBayesClassifier(instances)
        classifier.save( os.path.join(outputPath,"%s.nbc" % (relation)) )
        print "Write to %s %s.nbc" % (outputPath,relation)

if __name__ == "__main__":
    if len(sys.argv) > 2:
        modelsDir = sys.argv[1]
        outputPath = sys.argv[2]
        buildModels(modelsDir,outputPath)
    else:
        print "$ python ./buildNBCs.py [inpu model dir] [output model dir]"
