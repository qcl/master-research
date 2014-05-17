# -*- coding: utf-8 -*-
# qcl
# combined files viewer.

import os
import sys
import projizz
import simplejson as json

def combinedFileViewer(filename):
    
    content = projizz.combinedFileReader(filename)
  
    for articleName in content:
        article = content[articleName]
        print articleName.encode("utf-8")
        print ""
        for line in article:
            print line.encode("utf-8")
        print "----"


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        combinedFileViewer(filename)
    else:
        print "$ python ./combinedFilesViewer.py content.json"
