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
  
    start_time = datetime.now()
    for articleName in content:
        #print articleName
        article = projizz.articleSimpleLineFileter(content[articleName])
        
        for line in article:
            projizz._posTagger.tag(line)


        #print "\n----"
    diff = datetime.now() - start_time
    print "Spend %d.%d seconds" % (diff.seconds,diff.microseconds)

if __name__ == "__main__":
    testing("./000000.json")
