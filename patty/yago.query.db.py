# -*- coding: utf-8 -*-
# qcl

import pymongo
import projizz

def main():
    connect = pymongo.Connection()
    db = connect.projizz
    collection = db.patty.wiki.pattern

    model, table = projizz.readPrefixTreeModelWithTable("../yago/yagoPatternTree.model", "../yago/yagoPatternTree.table")
   
    for ptnId in table:
        ptnText = table[ptnId]["pattern"]
        queryRegexp = ptnText.replace("[","\\\\[").replace("]","\\\\]") + ";.*"
        itr = collection.find({"patterntext":{"$regex":queryRegexp}})
        print queryRegexp,itr.count()
        

if __name__ == "__main__":
    main()
