# -*- coding: utf-8 -*-
# qcl
# build yago model

import os
import simplejson as json

def buildYagoModel():

    model = {}

    for filename in os.listdir("./yagoRelation/"):
        if ".txt" in filename:
            f = open(os.path.join("./yagoRelation/%s" % (filename)),"r")
            for patternText in f:
                print patternText[:-2]
            f.close()



if __name__ == "__main__":
    buildYagoModel()
