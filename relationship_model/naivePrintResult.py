# -*- coding: utf-8 -*-
# qcl
# read output from ./naiveEval.py, output to stdout
import sys
import os
import simplejson as json

def main(inputResultFile,outputformat):

    filenames = []

    if not os.path.isdir(inputResultFile):
        filenames.append(inputResultFile)
    else:
        for f in os.listdir(inputResultFile):
            if ".out" in f:
                filenames.append(f)
    
    r = {}
    
    for filename in filenames:
        result = json.load(open(os.path.join(inputResultFile,filename),"r"))
        for model in result:
            m = result[model]

            if not model in r:
                r[model] = {"fp":0,"tn":0,"tp":0,"fn":0}
            j = r[model]
            j["tp"] += m["tp"]
            j["tn"] += m["tn"]
            j["fp"] += m["fp"]
            j["fn"] += m["fn"]

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
        
        m["p"] = pre
        m["r"] = rec
        m["a"] = acc
        m["n"] = model
        m["f"] = fsc
    
    # output
    for model in r:
        res = r[model]
        string = ""
        if outputformat[0] == "n":
            string = "%s" % (res["n"])
        elif outputformat[0] == "t":
            string = "%d\t%d\t%d\t%d" % (res["tp"],res["fn"],res["fp"],res["tn"] )
        else:
            string = "%.08f" % (res[outputformat[0]])

        for x in xrange(1,len(outputformat)):
            if outputformat[x] == "n":
                string += "\t%s" % (res[outputformat[x]])
            elif outputformat[x] == "t":
                string += "\t%d\t%d\t%d\t%d" % (res["tp"],res["fn"],res["fp"],res["fn"] )
            else:
                string += "\t%.08f" % (res[outputformat[x]])

        print string

if __name__ == "__main__":
    if len(sys.argv) > 2:
        inputResultFile = sys.argv[1]
        outputformat = sys.argv[2]
        main(inputResultFile,outputformat)
    else:
        print "$ python ./naivePrintResult.py input.json [prn|rpn|npr|nrp]"
        print "p = precision, r = recall, a = accuracy, f = f1, n = relationship name, t = tp,fn,fp,tn"
