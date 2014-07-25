# -*- coding: utf-8 -*-
# qcl

import os
import sys

def generageTable(filename,tableid):
    fp = open(filename,"r")

    prs = []

    for line in fp:
        l = line.split()
        if l[0] == "Average":

            prs.sort(key=lambda x:x["title"])


            marp = float(l[1])
            marr = float(l[2])
            mirp = float(l[3])
            mirr = float(l[4])
            if marp + marr > 0.0:
                marf = (2*marp*marr)/(marp+marr)
            else:
                marf = 0.0
            if mirp + mirr > 0.0:
                mirf = (2*mirp*mirr)/(mirp+mirr)
            else:
                mirf = 0.0
            prs.append({"title":"Macro Average", "p":l[1], "r": l[2], "f":marf})
            prs.append({"title":"Micro Average", "p":l[3], "r": l[4], "f":mirf})
        else:
            p = float(l[1])
            r = float(l[2])
            if p + r > 0.0:
                f = (2*p*r)/(p+r)
            else:
                f = 0.0
            prs.append({"title":l[0], "p":l[1], "r": l[2], "f":f})
    fp.close()

    print """\\begin{table}[t]
    \\begin{center}
        \small
        \\begin{tabular}{l||c|c||c}
        Property & Precision & Recall & $F_1$ Score \\\\ 
        \\hline"""
    
    for i in range(0,len(prs)-2):
        obj = prs[i]
        print "        %s & %s & %s & %.8f \\\\" % (obj["title"],obj["p"],obj["r"],obj["f"])

    print "        \\hline"
    for i in range(len(prs)-2,len(prs)):
        obj = prs[i]
        print "        %s & %s & %s & %.8f \\\\" % (obj["title"],obj["p"],obj["r"],obj["f"])
   
    print """        \end{tabular}
        \caption{TableTitle}
        \label{t:%s}
    \end{center}
\end{table}""" % (tableid)

if __name__ == "__main__":
    if len(sys.argv) > 2:
        filename = sys.argv[1]
        tableid = sys.argv[2]
        generageTable(filename,tableid)
    else:
        print "$ python ./genTexTable.py file.npr"
