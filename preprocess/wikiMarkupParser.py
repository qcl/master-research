# -*- coding: utf-8 -*-
# qcl
#
import sys
import os
import gc

def main(templateListFilename):

    # initialize template lists
    
    tempList = []

    f = open(templateListFilename,'r')
    for lines in f:
        tempList.append(lines.split(':')[1][:-1])
    sys.stderr.write("Read templates list.\n")
    f.close()

    title = ""
    tid   = ""

    c = 0
    fp = 0
    inPage = False
    inArticle = False

    inTmp = False
    
    inRef = False
    inLink = False

    found = 0
    
    link = ""
    
    template = ""
    content = ""
    deep = 0

    for line in sys.stdin:
        if line[:-1] == '  <page>':
            #if inPage:
            #    print line
            inPage = True
            inArticle = False
            found = False
            inTmp = False
            inRef = False
            inLink = False
            link = ""
            content = ""
            template = ""
            deep = 0
            found = 0
            gc.collect()
        elif line[:-1] == '  </page>':
            inPage = False
            inArticle = False
            c = c + 1


            if c > 0:
                break
            #if found:
            #    print line[:-1]
            #    fp = fp + 1
            #sys.stderr.write("read "+str(c)+" pages.\n")

        if inPage:
            if "    <title>" in line:
                title = line.split(">")[1].split("<")[0]
            elif "    <id>" in line:
                tid   = line.split(">")[1].split("<")[0]
            elif "      <text xml:space=\"preserve\">" in line:
                line = line.split("<text xml:space=\"preserve\">")[1]
                inArticle = True
                #print line
            elif "</text>" in line:
                line = line.split("</text>")[0]
                #print line
                inArticle = False

            if inArticle:

                lineString = line.replace("&lt;references/&gt;","")\
                    .replace("&lt;ref",chr(1))\
                    .replace("&lt;/ref&gt;",chr(2))\
                    .replace("{{",chr(3))\
                    .replace("}}",chr(4))\
                    .replace("[[",chr(5))\
                    .replace("]]",chr(6))\
                    .replace("&lt;!--",chr(7))\
                    .replace("--&gt;",chr(8))\
                    .replace("'''","")\
                    .replace("''","")

                #print lineString

                for char in lineString:

                    if char == chr(1) or char == chr(7):
                        inRef = True
                        continue
                    elif char == chr(2) or char == chr(8):
                        inRef = False
                        continue
                    elif char == chr(3):
                        inTmp = True
                        deep = deep + 1
                        #print "{{{"+str(deep)
                    elif char == chr(4):
                        deep = deep - 1
                        #print str(deep)+"}}}"
                        if deep == 0:
                            inTmp = False
                            if found == 1:
                                template = template+"}}"
                                print template
                            found = 0
                            #print "-}}}"
                            continue
                            
                    elif char == chr(5):
                        inLink = True
                        link = ""
                        continue
                    elif char == chr(6):
                        inLink = False
                        
                        link = link.split("|")
                        if len(link) == 1:
                            link = link[0]
                        else:
                            link = link[1]

                        if inTmp and found == 1:
                            template = template + link 

                        if not inTmp and not inRef:
                            print "[["+link+"]]"
                        continue
                       

                    if inRef:
                        continue
                    
                    if inTmp:
                        if found == 1:
                            if inLink:
                                link = link + char
                            else:
                                template = template + char
                            continue
                        elif found == 2:
                            continue
                        elif deep == 1:
                            #print "go!"
                            if found == 0:
                                for temp in tempList:
                                    if temp in lineString:
                                        found = 1
                                        break
                                if found == 0:
                                    #print 'not'
                                    found = 2
                                #else:
                                #    print 'found'
                            if found == 1:
                                template = "{{"
                                continue
                        else:
                            continue

                    else:
                        if inLink:
                            link = link + char
                        else:
                            print char,

                #if "{{" in line:
                #    for temp in tempList:
                #        if temp in line:
                #            found = True


                #    #num = len(line.split("{{")) - 1




                

            #if not found:
            #    content.append(line)
            #    
            #    if "{{" in line: 
            #        for temp in tempList:
            #            if temp in line:
            #                found = True
            #                for l in content:
            #                    print l[:-1]
            #else:
            #    print line[:-1]
        
    #sys.stderr.write("found "+str(fp)+" pages.\n")
    #print '<!-- ',fp,'/',c,'-->'




if __name__ == '__main__':
    if not len(sys.argv) == 2:
        print 'Usage: python wikiMarkupParser.py <templates list> < <input xml> > <output xml>'
    else:
        main(sys.argv[1])
    
