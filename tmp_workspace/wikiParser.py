# -*- coding: utf-8 -*-
# qcl
# wiki markup parser.

import gc
import sys
import os

def parse(wikiMarkUpString):

    ### Status ###
    
    # Template
    inTemplate = False
    templateDeep = 0

    # Reference
    inRef = False

    # Link

    # HTML Tag



    ### end of Stauts ###

    # Preprocessing
    wikiMarkUpString = wikiMarkUpString.replace("{{",chr(1))\
            .replace("}}",chr(2))\
            .replace("&lt;!--",chr(1))\
            .replace("--&gt;",chr(2))\
            .replace("&lt;references/&gt;","")\
            .replace("&lt;ref",chr(3))\
            .replace("&lt;/ref&gt;",chr(4))\
            .replace("'''","")\
            .replace("''","")

    result = ""

    for char in wikiMarkUpString:

        # decide status
        if char == chr(1):
            inTemplate = True
            templateDeep += 1
        elif char == chr(2):
            if inTemplate:
                if templateDeep > 0:
                    templateDeep -= 1
        elif char == chr(3):
            if not inTemplate:
                inRef = True

        # put or not put the char
        if inTemplate:
            pass
        elif inRef:
            pass
        else:
            result += char

        # decide status
        if templateDeep == 0:
            inTemplate = False

        if char == chr(4):
            inRef = False


    return result


if __name__ == '__main__':
    print "QCL's wiki parser demo"
    f = open("./wikitext.txt","r")
    s = ""
    for line in f:
        s+=line
    f.close()
    r = parse(s)
    print r
