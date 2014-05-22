# -*- coding: utf-8 -*-
# qcl
# build yago model

import os
import simplejson as json

def buildYagoModel():

    modelName = "yagoPatternTree"

    model = {}
    ptnId = 0
    table = {}

    for filename in os.listdir("./yagoRelation/"):
        relationName = filename[:-4]
        print relationName
        if ".txt" in filename:
            f = open(os.path.join("./yagoRelation/%s" % (filename)),"r")
            for patternText in f:
                ws = patternText[:-2].split()
                t = model
                for w in ws:
                    if not w in t:
                        t[w] = {}
                    t = t[w]

                if "_id_" in t:
                    ptnData = table[t["_id_"]]
                    if not relationName in ptnData["relation"]:
                        ptnData["relation"].append(relationName)
                else:
                    ptnId += 1
                    t["_id_"] = ptnId
                    table[ptnId] = {"pattern":patternText[:-2],"relation":[relationName]}

            f.close()
    
    # test
    pid = model["to"]["play"]["in"]["_id_"]
    print table[pid]
    print len(table)

    json.dump(model,open(os.path.join("%s.model" % (modelName)),"w"))
    json.dump(model,open(os.path.join("%s.table" % (modelName)),"w"))
    
    f = open(os.path.join("%s.table.txt" % (modelName)),"w")
    for i in xrange(1,ptnId+1):
        f.write("%d\t%s %d %s\n" % (i,table[i]["pattern"],len(table[i]["relation"]),table[i]["relation"]))
    f.close()
    
    f = open(os.path.join("%s.pattern.overlap" % (modelName)),"w")
    overlapPattern = sorted(table.iteritems(),key=lambda x:len(x[1]["relation"]),reverse=True)
    for i,t in overlapPattern:
        f.write("%d\t%s %d %s\n" % (i,t["pattern"],len(t["relation"]),t["relation"]))
    f.close()


if __name__ == "__main__":
    buildYagoModel()
