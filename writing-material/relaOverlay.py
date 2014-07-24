# -*- coding: utf-8 -*-
# qcl
# using table information to calculate overlay of each relation

import projizz

def calculateOverlay():
    model, table = projizz.readPrefixTreeModelWithTable("../yago/yagoPatternTree.model", "../patty/yagoPatternTreeWithConfidence.table")
    
    overlay = {}
    for relation in projizz.getYagoRelation():
        overlay[relation] = {}
        for rela in projizz.getYagoRelation():
            overlay[relation][rela] = 0

    # Build table
    for pid in table:
        if table[pid]["used"]:
            if "eval" in table[pid] and not table[pid]["eval"]:
                continue
            for relation in table[pid]["relations"]:
                for rela in table[pid]["relations"]:
                    overlay[relation][rela] += 1
        else:
            pass

    yagoRela = projizz.getYagoRelation()
    yagoRela.sort()
    yagoRela.remove("produced")

    #print yagoRela

    print "      ",
    for i in range(13,25):
        print "& (%d)" % (i),
    print "\\\\"

    for relaA in yagoRela:
        j = []
        for relaB in yagoRela:
            overC = overlay[relaA][relaB]
            j.append((relaB,overC))
        #j.sort(key=lambda x:x[1],reverse=True)
        a = overlay[relaA][relaA]
        _id = yagoRela.index(relaA) + 1
        print "(%d) %s" % (_id,relaA),
        for relaB,overC in j:
            b = overlay[relaB][relaB]
            _tid = yagoRela.index(relaB) + 1
            if _tid < 13:
                continue
            #print "%s(%d) -> %s(%d) %d/%d %.5f (%d/%d,%.5f)" % (relaA,_id,relaB,b,overC,a,float(overC)/a,overC,b,float(overC)/b)
            print " & %2.2f" % (float(overC)/a),
        print "\\\\"

if __name__ == "__main__":
    calculateOverlay()
