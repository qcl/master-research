# -*- coding: utf-8 -*-
# extract template name, id, article, and possible templates
# usage: python ./buildTableAndFindTemplates.py < .split.xml > table.csv
import sys
import os

# pares template in string
def getTemplateInString(string):
    if "{{" in string and "}}" in string:
        return True
    else:
        return False

# parse key, value
#  | key   = value
def getKeyAndValueInTemplate(string,tid):
    if "=" in string:
        return string[:string.index("=")].replace(" ","")
    else:
        return ""

def parseInput():
    
    # states
    inTemplate = False
    inTitle = False
    inID = False
    inContent = False

    firstLine = False
    errorThenPass = False

    # attributes
    title = ""
    tid = ""
    templateName = ""

    keys = []

    for line in sys.stdin:
        
        # states
        if "<title>" in line:
            inTitle = True
            continue
        elif "</title>" in line:
            inTitle = False
            continue
        elif "<id>" in line:
            inID = True
            continue
        elif "</id>" in line:
            inID = False
            continue
        elif "<template>" in line:
            inTemplate = True
            firstLine = True
            continue
        elif "</template>" in line:
            inTemplate = False
            continue
        elif "<content>" in line:
            inContent = True
            firstLine = True
            continue
        elif "</content>" in line:
            inContent = False
            if firstLine:
                errorThenPass = True
            continue
        
        # end of page
        elif "</page>" in line:
            if errorThenPass:
                errorThenPass = False
            else:
                while templateName[-1] == " " or ord(templateName[-1]) == 8 or templateName[-1] == "|":
                    templateName = templateName[:-1]
                print "\"%s\",\"%s\",\"%s\"" % (tid,title,templateName.lower())

        if inTitle:
            title = line[:-1]
        elif inID:
            tid = line[:-1]
        elif inTemplate:
            if firstLine:
                if not "}}" in line:
                    templateName = line[10:-1]
                else:
                    lineContent = line[:-1].split("|")
                    tmp = lineContent[0].split()
                    name = ""
                    if len(tmp) > 1 and "{{Infobox" in tmp[0]:
                        for i in range(1,len(tmp)):
                            name = name + tmp[i] + " "
                        name = name[:-1]
                    if len(name) > 0:
                        templateName = name
                        #print tid,title,templateName,line
                    else:
                        errorThenPass = True
                firstLine = False
            else:
                pass
                #if getTemplateInString(line[:-1]):
                #    print line[:-1]
                
                if "|" in line[:-1]:
                    s = line[line.index("|")+1:-1]
                    k = getKeyAndValueInTemplate(s,tid)
                    if not k in keys:
                        keys.append(k)


        elif inContent:
            if firstLine:
                firstLine = False
            pass

    #print keys

if __name__ == "__main__":
    parseInput()
