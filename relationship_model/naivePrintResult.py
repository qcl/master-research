# -*- coding: utf-8 -*-
# qcl
# read output from ./naiveEval.py, output to stdout
import sys
import os
import simplejson as json

def main(inputResultFile,outputformat):
    result = json.load(open(inputResultFile,"r"))
    r = {}
    for model in result:
        m = result[model]
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
        r[model] = {"p":pre,"r":rec,"a":acc,"n":model,"f":fsc}
    
    for model in r:
        res = r[model]
        string = ""
        if outputformat[0] == "n":
            string = "%s" % (res["n"])
            if len(res["n"]) < 4:
                string += "\t"
            if len(res["n"]) < 8:
                string += "\t"
            if len(res["n"]) < 12:
                string += "\t"
            if len(res["n"]) < 16:
                string += "\t"
            if len(res["n"]) < 20:
                string += "\t"
            if len(res["n"]) < 24:
                string += "\t"

        else:
            string = "%.08f" % (res[outputformat[0]])

        for x in xrange(1,len(outputformat)):
            if outputformat[x] == "n":
                string += "\t%s" % (res[outputformat[x]])
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
        print "p = precision, r = recall, a = accuracy, f = f1, n = relationship name"
