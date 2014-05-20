# -*- coding: utf-8 -*-
# qcl
# combined files viewer.

import os
import sys
import projizz
import simplejson as json

from datetime import datetime

def testing(filename):
    
    content = projizz.combinedFileReader(filename)

    model, table = projizz.readPrefixTreeModel("./../prefix_tree_model/patternTree.json")
  
    start_time = datetime.now()
    for articleName in content:
        print articleName
        article = projizz.articleSimpleSentenceFileter(content[articleName])
        
        for line in article:
            tokens = projizz._posTagger.tag(line)
            patternExtracted = projizz.naiveExtractPatterns(tokens,model)
            if len(patternExtracted)>0:
                print line.encode("utf-8")
                for ptnId,start,to in patternExtracted:
                    print "\t[%d] %s" % (ptnId,table[ptnId]["pattern"])

        print "\n----"
    diff = datetime.now() - start_time
    print "Spend %d.%d seconds" % (diff.seconds,diff.microseconds)

if __name__ == "__main__":
    testing("./000000.json")
