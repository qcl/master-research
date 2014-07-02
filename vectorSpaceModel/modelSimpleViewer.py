# -*- coding: utf-8 -*-
# qcl
# view the sorted tf-idf weight

import projizz
import os
import sys

def viewer(path,threshold):
    model = projizz.jsonRead(path)
    sortedModel = sorted(model.items(), key=lambda x:x[1], reverse=True)
    for word, score in sortedModel:
        if score >= threshold:
            print "%s\t%f" % (word.encode("utf-8"),score)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        tfidfWeightFilePath = sys.argv[1]
        if len(sys.argv) > 2:
            threshold = float(sys.argv[2])
        else:
            threshold = 0.0
        viewer(tfidfWeightFilePath,threshold)
    else:
        print "$ python ./modelSimpleViewer.py [tfidfModel.json] (threshold)"
