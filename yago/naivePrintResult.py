# -*- coding: utf-8 -*-
# qcl
# read output from ./naiveEval.py, output to stdout
import sys
import os
import simplejson as json

def main(inputResultFile):

    filenames = []

    if not os.path.isdir(inputResultFile):
        filenames.append(inputResultFile)
        inputResultFile = "./"
    else:
        for f in os.listdir(inputResultFile):
            if ".out" in f:
                filenames.append(f)
    
    
    precision = {}
    recall    = {}

    for filename in filenames:
        r = {}
        result = json.load(open(os.path.join(inputResultFile,filename),"r"))
        for model in result:
            m = result[model]

            if not model in r:
                r[model] = {"fp":0,"tn":0,"tp":0,"fn":0}
            if not model in precision:
                precision[model] = []
            if not model in recall:
                recall[model] = []


            j = r[model]
            j["tp"] += len(m["tp"])
            j["tn"] += len(m["tn"])
            j["fp"] += len(m["fp"])
            j["fn"] += len(m["fn"])
            #print model,"tp",len(m["tp"]),m

    

        for model in r:
            m = r[model]

            if float(m["tp"]+m["fp"]) == .0:
                pre = .0
            else:
                pre = float(m["tp"])/float(m["tp"]+m["fp"])

            if float(m["tp"]+m["fn"]) == .0:
                rec = .0
            else:
                rec = float(m["tp"])/float(m["tp"]+m["fn"])
        
            if float(m["tp"]+m["tn"]+m["fp"]+m["fn"]) == .0:
                acc = .0
            else:
                acc = float(m["tp"]+m["tn"])/float(m["tp"]+m["tn"]+m["fp"]+m["fn"])
        
            if pre+rec == .0:
                fsc = .0
            else:
                fsc = (2*pre*rec)/(pre+rec)
        
            precision[model].append(pre)
            recall[model].append(rec)
    
    # output
    for model in precision:
        string = ""
        for i in range(0,len(precision[model])):
            string += "\t%.08f\t%0.08f" % (precision[model][i],recall[model][i])

        string = "%s\t\%.08f\t%.08f" % (model,sum(precision[model])/float(len(precision[model])),sum(recall[model])/float(len(recall[model]))) + string

        print string

if __name__ == "__main__":
    if len(sys.argv) > 1:
        inputResultFile = sys.argv[1]
        main(inputResultFile)
    else:
        print "$ python ./naivePrintResult.py input-dir"
