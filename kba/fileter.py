# -*- coding: utf-8 -*-
# qcl
#
# fileter KBA'13 Data

import os
import sys
import streamcorpus
import multiprocessing
from datetime import datetime
from streamcorpus.ttypes_v0_2_0 import StreamItem as StreamItem_v0_2_0

def fileter(path):

    print "fileter",path

    chunk = None
    founds = []
    try:
        chunk = streamcorpus.Chunk(path=path, message=StreamItem_v0_2_0)
        for si in chunk:
            lang = si.body.language
            #if lang == None:
            #    continue
            #if not lang.code == "en":
            #    continue
            
            ratings = si.ratings
            if len(ratings) <= 0:
                continue
            
            doc_id = si.doc_id

            _found = False
            for annotator in ratings:
                a_ratings = ratings[annotator]
                for rating in a_ratings:
                    if rating.target.target_id == None:
                        continue
                    #print doc_id,rating.target.target_id,rating.relevance,rating.contains_mention
                    _found = True
                    break
                if _found:
                    founds.append(si)
                    break
        print "fileter found %d StreamItem in %s" % (len(founds),path)
    except:
        print "fileter cannot read",path

    return founds

def scanDir(tid,pathBase,dirname,outputPath):
    
    dirpath = os.path.join(pathBase,dirname)

    if os.path.isdir(dirpath):
        for filename in os.listdir(dirpath):
            #print filename
            founds = fileter(os.path.join(dirpath,filename))
            if len(founds) > 0:
                if not os.path.isdir(os.path.join(outputPath,dirname)):
                    os.mkdir(os.path.join(outputPath,dirname))
                try:
                    ch = streamcorpus.Chunk("%s.sc" % (os.path.join(outputPath,dirname,filename)), mode="wb", message=StreamItem_v0_2_0 )
                    for si in founds:
                        ch.add(si)
                    ch.close()
                    print "%d write to %s" % (tid,os.path.join(outputPath,dirname,filename))
                except:
                    print "[Fail] %d write to %s" % (tid,os.path.join(outputPath,dirname,filename))

def main(kbaBasePath,dirlist,outputPath):
   
    dirs = []

    f = open(dirlist,"r")
    for line in f:
        dirs.append(line[:-1])

    cpus = multiprocessing.cpu_count() 
    print "total %d dirs, %s cpus" % (len(dirs),cpus)

    pool = multiprocessing.Pool(processes=cpus)
    start_time = datetime.now()

    t = 0
    for dirname in dirs:
        pool.apply_async(scanDir, (t,kbaBasePath,dirname,outputPath))
        t += 1

    pool.close()
    pool.join()
    
    diff = datetime.now() - start_time
    print "Spend %d.%d seconds" % (diff.seconds, diff.microseconds)



if __name__ == "__main__":
    if len(sys.argv) > 3:
        kbaBasePath = sys.argv[1]
        dirlist = sys.argv[2]
        outputPath = sys.argv[3]
        main(kbaBasePath,dirlist,outputPath)
    else:
        print "$ python [kba-base-path] [dir-list-file] [output-path]"

        #print "Demo"
        #fileter("../../streamcorpus/test-data/john-smith-tagged-by-lingpipe-0-v0_2_0.sc.xz")
        #scanDir(1,"../../streamcorpus/","test-data", "/Users/qcl/git")
        #fileter("../../test-data/john-smith-tagged-by-lingpipe-0-v0_2_0.sc.xz.sc")

