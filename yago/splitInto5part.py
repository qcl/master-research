# -*- coding: utf-8 -*-
# qcl
import os
import shutil

def splitTo5part(rootPath,originAll,targetPath,prefix):

    files = []
    for filename in os.listdir(os.path.join(rootPath,originAll)):
        if ".json" in filename:
            files.append(filename)
    files.sort()

    count = 0
    for filename in files:
        targetDirName = "%s-part-%d" % (prefix,count%5)
        print "%s -> %s-part-%d" % (filename,prefix,count%5)
        if not os.path.isdir(os.path.join(targetPath,targetDirName)):
            os.mkdir(os.path.join(targetPath,targetDirName))
        count += 1
        shutil.copy2(os.path.join(rootPath,originAll,filename),os.path.join(targetPath,targetDirName))

if __name__ == "__main__":
    splitTo5part("/home/ccli/nas-3/yago","yago-all","/home/ccli/nas-3/yago","yago")
    splitTo5part("/home/ccli/nas-3/yago-ptn","yago-ptn-all","/home/ccli/nas-3/yago-ptn","yago-ptn")
