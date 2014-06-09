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

    for relaA in projizz.getYagoRelation():
        j = []
        for relaB in projizz.getYagoRelation():
            overC = overlay[relaA][relaB]
            j.append((relaB,overC))
        j.sort(key=lambda x:x[1],reverse=True)
        a = overlay[relaA][relaA]
        for relaB,overC in j:
            b = overlay[relaB][relaB]
            print "%s(%d) -> %s(%d) %d/%d %.5f (%d/%d,%.5f)" % (relaA,a,relaB,b,overC,a,float(overC)/a,overC,b,float(overC)/b)

if __name__ == "__main__":
    calculateOverlay()
