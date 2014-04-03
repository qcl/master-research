# -*- coding: utf-8 -*-
# qcl
#
import sys
import os
import gc

def main(idList):

    # initialize template lists

    f = open(idList,'r')
    targetID = f.readline()[:-1]
    
    inPage = False
    inArticle = False

    for line in sys.stdin:
        if line[:-1] == '  <page>':
            #if inPage:
            #    print line
            inPage = True
            inArticle = False
            needPass = False
            content = ""
            gc.collect()
        elif line[:-1] == '  </page>':
            inPage = False
            inArticle = False

            #fp = fp + 1
            #sys.stderr.write("#"+str(c)+" "+title+"("+tid+").\n")

        if inPage:
            if "    <title>" in line:
                title = line.split(">")[1].split("<")[0]
            elif "    <ns>" in line:
                beforeNS = True
            elif "    <id>" in line and beforeNS:
                tid   = line.split(">")[1].split("<")[0]
                if tid == targetID:
                    targetID = f.readline()[:-1]
                    sys.stderr.write("Found "+title+"("+tid+").\n")
                else:
                    needPass = True

                beforeNS = False
            elif "      <text xml:space=\"preserve\">" in line:
                line = line.split("<text xml:space=\"preserve\">")[1]
                inArticle = True
                #print line

                if not needPass:
                    content = content + line

            elif "</text>" in line:
                line = line.split("</text>")[0]
                inArticle = False

                if not needPass:
                    content = content + line

                    print "<page>\n<title>\n"+title+"\n</title>\n<id>\n"+tid+"\n</id>"
                    print "<content>"
                    print content
                    print "</content>\n</page>"
            
            if inArticle and not needPass:
                content = content + line
        


    f.close()


if __name__ == '__main__':
    if not len(sys.argv) == 2:
        print 'Usage: python parsePageById.py <idList> < <input xml> > <output xml>'
    else:
        main(sys.argv[1])
    
