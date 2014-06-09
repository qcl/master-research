# -*- coding: utf-8 -*-
# qcl
# parse yago pattern data from patty website
# It's for finding the confidence value of each pattern.
# 可以順便建立Pattern Overlay 和Ambiguity Degree

import projizz

def parseYagoData():
    
    phase = "used"
    
    if phase == "build":
        model, table = projizz.readPrefixTreeModelWithTable("../yago/yagoPatternTree.model", "../yago/yagoPatternTree.table")
    else:
        model, table = projizz.readPrefixTreeModelWithTable("../yago/yagoPatternTree.model", "./yagoPatternTreeWithConfidence.table")
    
    # function testing.
    #test = "has appeared like [[num]]"
    ##test = "has appeared like [[num]"
    #i = projizz.naiveMatchPattern(test,model) 
    #print i


    a = table.keys()
    originL = len(a)

    ptnByRelation = {}

    

    for relation in projizz.getYagoRelation():
        if not phase == "build":
            break
        
        f = open("./yagoRela/%s.txt" % (relation))
        
        print relation

        text = f.readline()
        ptnSynsetTxt = text.split("\",\" ")[1:]
        ptnSynsetTxt = ptnSynsetTxt[:-1] + [ ptnSynsetTxt[-1][:-7] ]

        ptnByRelation[relation] = []
        

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
                    pid = str(pid)
                    if pid in a:
                        a.remove(pid)
                    if not pid in ptnByRelation[relation]:
                        ptnByRelation[relation].append(pid)

                    if not relation in table[pid]["relations"]:
                        table[pid]["relations"].append(relation)
                        #print relation,pid,pattern

                    ptnS = table[pid]
                    if not "confidence" in ptnS:
                        table[pid]["confidence"] = float(ptns[6])
                        table[pid]["support"] = int(ptns[7])
                        table[pid]["used"] = True
            
                        if len(ptns) > 8:
                            if ptns[8] == "false":
                                table[pid]["eval"] = False
                                #print pid,table[pid]["relations"],pattern,ptns[8]
                            else:
                                table[pid]["eval"] = True

        f.close()

    if phase == "build":

        for pid in a:
            table[pid]["used"] = False
    
        for pid in table:
            if table[pid]["used"]:
                needRemove = []
                for relation in table[pid]["relations"]:
                    if not pid in ptnByRelation[relation]:
                        print pid,table[pid]["pattern"],relation
                        needRemove.append(relation)
                for p in needRemove:
                    table[pid]["relations"].remove(p)
                if len(table[pid]["relations"]) == 0:
                    print pid,table[pid]["pattern"],"!!!"
            else:
                pass

        projizz.jsonWrite(table,"./yagoPatternTreeWithConfidence.table")

    else:
        c = 0
        for pid in table:
            if table[pid]["used"]:
                for relation in table[pid]["relations"]:
                    if not relation in ptnByRelation:
                        ptnByRelation[relation] = []
                    if not pid in ptnByRelation[relation]:
                        ptnByRelation[relation].append(pid)
            else:
                c += 1

    # 一些小計算
    for relation in ptnByRelation:
        print relation,len(ptnByRelation[relation])
    
    # 找最高（意思就是不能再更高了）信心值
    # 每組Relation的最高之中最小的那一個


if __name__ == "__main__":
    parseYagoData()
