# -*- coding: utf-8 -*-
# qcl
# projizz I/O prefix tree model

import simplejson as json

def readModel(treeModelPath):
    treeModel = json.load(open(treeModelPath,"r"))
    return treeModel

if __name__ == "__main__":
    print "projizzTreeModel.py demo"

