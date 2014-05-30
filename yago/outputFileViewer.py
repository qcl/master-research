# -*- coding: utf-8 -*-
# qcl

# python ./outputFileViewer.py .out relation [tn|tp|fn|fp]


import simplejson as json
import sys

result = json.load(open(sys.argv[1],"r"))

relationResult = result[sys.argv[2]]

files = relationResult[sys.argv[3]]

print sys.argv[2],"->",sys.argv[3],"count:",len(files)
for revid in files:
    print revid
