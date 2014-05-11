# -*- coding: utf-8 -*-
# qcl
# viewer of the treeEval result

import os
import sys
import simplejson as json

if len(sys.argv) > 2:
    filepath = sys.argv[1]
    query = sys.argv[2]
    if os.path.isdir(filepath): 
        result = {}
        for filename in os.listdir(filepath):
            if ".out" in filename or ".txt" in filename:
                r = json.load(open(os.path.join(filepath,filename),"r"))
                for port in r:
                    if not port.lower() == query.lower():
                        continue
                    if not port in result:
                        result[port] = {"fp":[],"tp":[],"tn":[],"fn":[]}
                    result[port]["fp"] += r[port]["fp"]
                    result[port]["tp"] += r[port]["tp"]
                    result[port]["fn"] += r[port]["fn"]
                    result[port]["tn"] += r[port]["tn"]

    else:
        result = json.load(open(filepath),"r")

    for port in result:
        if port.lower() == query.lower():
            print port
            print ""
            print "True Postive",len(result[port]["tp"])
            print result[port]["tp"]
            print ""
            print "False Negative",len(result[port]["fn"])
            print result[port]["fn"]
            print ""
            print "False Postive",len(result[port]["fp"])
            print result[port]["fp"]
            print ""
            print "True Negative",len(result[port]["tn"])
            print result[port]["tn"]
            print ""
    
