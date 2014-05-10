# -*- coding: utf-8 -*-
# qcl
# viewer of the treeEval result

import os
import sys
import simplejson as json

if len(sys.argv) > 1:
    result = json.load(open(sys.argv[1]),"r")
    
