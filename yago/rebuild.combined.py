# -*- coding: utf-8 -*-
# qcl
# rebuild combined yago file, and split into 5 parts for 5 cv

import simplejson as json
import projizz
import os
import sys

def combined():
    files = []
    for filename in os.listdir("/home/ccli/nas-3/yago/yago-json-part-a/"):
        if ".json" in filename:
            files.append("/home/ccli/nas-3/yago/yago-json-part-a/%s" % (filename))
    for filename in os.listdir("/home/ccli/nas-3/yago/yago-json-part-b"):
        if ".json" in filename:
            files.append("/home/ccli/nas-3/yago/yago-json-part-b/%s" % (filename))

    files.sort()

    if not os.path.isdir("/home/ccli/nas-3/yago/yago-all/"):
        os.mkdir("/home/ccli/nas-3/yago/yago-all")
    if not os.path.isdir("/home/ccli/nas-3/yago-ptn/yago-ptn-all"):
        os.mkdir("/home/ccli/nas-3/yago-ptn/yago-ptn-all")
    count = 0;
    f = open("/home/ccli/nas-3/yago/yago-all/%05d.json" % (count),"w")
    fptn = open("/home/ccli/nas-3/yago-ptn/yago-ptn-all/%05d.json" % (count),"w")
    
    tmpC = {}
    tmpPtn = {}

    fc = 0
    for filename in files:
        fc += 1
        print "%s %d / %d" % (filename.split("/")[-1],fc,len(files))
        g = json.load(open(filename,"r"))
        if "json-part-a" in filename:
            gptn = json.load(open("/home/ccli/nas-3/yago-ptn/yago-ptn-a/%s" % (filename.split("/")[-1]),"r"))
        else:
            gptn = json.load(open("/home/ccli/nas-3/yago-ptn/yago-ptn-b/%s" % (filename.split("/")[-1]),"r"))

        for key in g: 
            tmpC[key] = g[key]
            tmpPtn[key] = gptn[key]

            if len(tmpC) == 1000:
                print "wirte to %05d.json" % (count)
                json.dump(tmpC,f)
                json.dump(tmpPtn,fptn)
                tmpC = {}
                tmpPtn = {}
                f.close()
                fptn.close()
                count += 1
                f = open("/home/ccli/nas-3/yago/yago-all/%05d.json" % (count),"w")
                fptn = open("/home/ccli/nas-3/yago-ptn/yago-ptn-all/%05d.json" % (count),"w")

    if len(tmpC) > 0: 
            json.dump(tmpC,f)
            json.dump(tmpPtn,fptn)
            tmpC = {}
            tmpPtn = {}
            f.close()
            fptn.close()

    print "write %d files" % (count)
if __name__ == "__main__":
    combined()
