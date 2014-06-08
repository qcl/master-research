# -*- coding: utf-8 -*-
# qcl
# parse yago pattern data from patty website
# It's for finding the confidence value of each pattern.

import projizz

def parseYagoData():
    model, table = projizz.readPrefixTreeModelWithTable("../yago/yagoPatternTree.model", "../yago/yagoPatternTree.table")
    
    # function testing.
    #test = "has appeared like [[num]]"
    ##test = "has appeared like [[num]"
    #i = projizz.naiveMatchPattern(test,model) 
    #print i

    a = table.keys()

    for relation in projizz.getYagoRelation():
        f = open("./yagoRela/%s.txt" % (relation))
        
        text = f.readline()
        ptnSynsetTxt = text.split("\",\" ")[1:]
        ptnSynsetTxt = ptnSynsetTxt[:-1] + [ ptnSynsetTxt[-1][:-7] ]

        

        evC = 0
        for text in ptnSynsetTxt:
            ptns = text.split("#")
            # ptns[1] : pattern synset id in patty
            # ptns[3] : pattern domain
            # ptns[4] : pattern plain text
            # ptns[5] : pattern range
            # pnts[6] : confidence
            # ptns[7] : support co-occurrence
            # ptns[8] : some has, I guess it is eval result.
            if len(ptns) > 8:
                evC += 1

            patterns = ptns[4].split(";%")
            patterns = patterns[:-1] + [patterns[-1][:-1]]

            for pattern in patterns:
                pid = projizz.naiveMatchPattern(pattern,model)
                if pid < 0:
                    pass
                    #print relation,pattern
                else:
                    if str(pid) in a:
                        a.remove(str(pid))
        f.close()

    print a,len(a)

if __name__ == "__main__":
    parseYagoData()
