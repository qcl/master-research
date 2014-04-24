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
        pre = float(m["tp"])/float(m["tp"]+m["fp"])
        rec = float(m["tp"])/float(m["tp"]+m["fn"])
        acc = float(m["tp"]+m["tn"])/float(m["tp"]+m["tn"]+m["fp"]+m["fn"])
        fsc = (2*pre*rec)/(pre+rec)
        r[model] = {"p":pre,"r":rec,"a":acc,"n":model,"f":fsc}
    
    for model in r:
        res = r[model]
        string = ""
        if outputformat[0] == "n":
            string = "%s" % (res["n"])
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
