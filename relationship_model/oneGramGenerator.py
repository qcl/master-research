# -*- coding: utf-8 -*-
# qcl

# Generate 1-gram (that is, word feq) from dir

import os
import gc
import sys
import nltk
import operator
import json

def oneGramByFile(inputFileName):
    print "File:%s" % (inputFileName)
    f = open(inputFileName,"r")
    words = {}
    for line in f:
        tokens = nltk.word_tokenize(line)
        for token in tokens:
            if not token in words:
                words[token] = 0
            words[token] += 1
    f.close()
    return words


def main(source,target):
    for f in os.listdir(source):
        if ".txt" in f:
            gram = oneGramByFile(os.path.join(source,f))
            g = open("%s.1g.json" % (os.path.join(target,f.split(".txt")[0])) , "w")
            json.dump(gram,g)
            g.close()
     

if __name__ == "__main__":
    # gen 1-gram from source/*.txt then save it to target dir
    if len(sys.argv) >= 3:
        source = sys.argv[1]
        target = sys.argv[2]
        if len(sys.argv) > 3:
            isStem = True

        main(source,target)

    else:
        print "$ python ./oneGramGenerator.py [source dir] [target dir] (stemming)"
