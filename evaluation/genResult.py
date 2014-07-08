# -*- coding: utf-8 -*-
# qcl

import os
import sys

def gen(path,target):

    if not os.path.isdir(target):
        os.mkdir(target)

    hasChildDir = False
    if not os.path.isdir(path):
        return
    for f in os.listdir(path):
        if os.path.isdir(os.path.join(path,f)):
            hasChildDir = True
            break

    if hasChildDir:
        for f in os.listdir(path):
            if os.path.isdir(os.path.join(path,f)):
                i = os.path.join(path,f)
                o = os.path.join(target,f.split("/")[-1])
                print i,o
                os.system("python ./calPRF.py %s > %s.npr" % (i,o))
    else:
        f = path.split("/")[-1]
        os.system("python ./calPRF.py %s > %s.npr" % (path,os.path.join(target,f)))

if __name__ == "__main__":
    if len(sys.argv) > 2:
        path = sys.argv[1]
        target = sys.argv[2]
        gen(path,target)
    else:
        print "$ python ./genResult.py dir output-dir"
