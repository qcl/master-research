# -*- coding: utf-8 -*-
"""
projizz by qcl
create: 2014.05.17
modify: 2014.06.26

The python library for operation Projizz.
Add this to the $PYTHONPATH.
"""
#
#   Imports
#
import os
import re
import nltk
import copy
import simplejson as json

from .yago import relations as yagoRelations
from .dbpedia import relations as dbpediaRelations
from .yagoRelation import yagoDomainRange

from textblob import TextBlob
from textblob_aptagger import PerceptronTagger

from nltk.corpus import stopwords
#
#   Variables
#
__author__ = "Qing-Cheng Li <qc.linux@gmail.com>"
__version__ = "0.1"

_removeRefWords = re.compile(r"\[\d+\]") 
_naiveSentenceSpliter = re.compile(r"\.\s+|\!\s+|\?\s+")

_posTagger = PerceptronTagger()

_stopwords = stopwords.words("english")

#
#   Functions
#

# Combined Files
def combinedFileReader(filename):
    """combinedFileReader
    return {"sub-filename":[content of file]}
    """
    f = open(filename,"r")
    articles = json.load(f)
    f.close()
    return articles

def combinedFileWriter(obj,filename):
    """combinedFileWriter
    write out
    """
    f = open(filename,"w")
    json.dump(obj,f)
    f.close()

def jsonRead(filename):
    return combinedFileReader(filename)

def jsonWrite(obj,filename):
    return combinedFileWriter(obj,filename)

def getNaiveSentences(text):
    """getNaiveSentences
    return a list of sentences
    """
    return _naiveSentenceSpliter.split(text)

def articleSimpleLineFileter(article,tokenThreshold=5):
    """articleSimpleLineFileter
    input: article (list of lines)
    return filtered article (list of lines)
    """
    fileteredLines = []
    for line in article:
        if len(line.split()) > tokenThreshold:
            fileteredLines.append( removeRefWords(line) )
    return fileteredLines 

def articleSimpleSentenceFileter(article,tokenThreshold=5):
    """articleSimpleSentenceFileter
    input: article (list of lines)
    return filtered article (list of lines)
    """
    fileteredLines = []
    for line in article:
        if len(line.split()) > tokenThreshold:
            sents = getNaiveSentences(line)
            for sent in sents:
                string = removeRefWords(sent)
                if len(string.split()) > tokenThreshold:
                    fileteredLines.append(string)

    return fileteredLines

def getNaivePOSTagName(pos):
    """getNaivePOSTagName
    input: POS tag name 
    return the POS tag name of PATTY
    """
    tagName = "_na_"
    if pos[-2:] == "DT":    # [[det]]
        tagName = "[[det]]"
    elif pos[:2] == "JJ":   # [[adj]]
        tagName = "[[adj]]"
    elif pos[:3] == "PRP":  # [[pro]]
        tagName = "[[pro]]"
    elif pos == "CD":       # [[num]]
        tagName = "[[num]]"
    elif pos == "CC":       # [[con]]
        tagName = "[[pos]]"
    elif pos == "MD":       # [[mod]]
        tagName = "[[mod]]"
    elif pos == "IN":       # [[prp]]
        tagName = "[[prp]]"
    elif pos[:2] == "NN":   # [[_n_]]   for suffix N
        tagName = "[[_n_]]"
    return tagName

def removeRefWords(string):
    """removeRefWords
    remove [num]
    """
    return _removeRefWords.sub("",string)

def getNaiveToken(string):
    """getNaiveToken
    return list of words
    """
    return removeRefWords(string).split()

def removeStopwords(tokens):
    """removeRefWords
    input a tokens list, return a list that has no stopwords
    """
    _tokens = []
    for token in tokens:
        _token = token.lower()
        if not _token in _stopwords:
            _tokens.append(_token)

    return _tokens

def readPrefixTreeModelWithTable(modelJsonPath,tableJsonPath):
    """readPrefixTreeModelWithTable
    read modle and table
    """
    f = open(modelJsonPath,"r")
    model = json.load(f)
    f.close()

    f = open(tableJsonPath,"r")
    table = json.load(f)
    f.close()

    return model,table

def readPrefixTreeModel(modelJsonPath):
    """readPrefixTreeModel
    return the prefix tree model from pattern tree .json file
    """
    f = open(modelJsonPath,"r")
    model = json.load(f)
    f.close()
   
    idTable = {}

    # add pattern ID into pattern tree and build a id-to-pattern table
    def _trackTree(node):
        for leaf in node:
            if leaf == "_ptn_":
                ptnId = len(idTable)
                idTable[ptnId] = {
                        "pattern": node["_ptn_"],
                        "relations" : node["_rls_"]
                        }
            elif leaf == "_rls_":
                pass
            elif leaf == "_rid_":
                pass
            else:
                _trackTree(node[leaf])
  
    _trackTree(model)

    for ptnId in idTable:
        pattern = idTable[ptnId]["pattern"].replace(";","").lower().split()
        t = model
        for word in pattern:
            t = t[word]
        t["_id_"] = ptnId

    return model, idTable

def naiveMatchPattern(ptnPlainText,model):
    m = model
    t = ptnPlainText.split(" ")
    ptnId = -1
    found = True
    for token in t:
        if token in m:
            m = m[token]
        else:
            found = False
            break

    if "_id_" in m and found:
        ptnId = m["_id_"]

    return ptnId

def naiveExtractPatternsFromListOfWords(words,model):
    return naiveExtractPatterns(zip(words,["_na_"]*len(words)),model,usePos=False)

def naiveExtractPatterns(tokens,model,usePos=True):
    """naiveExtractPatterns
    tokens: list of (word, pos-tag)
    model: tree modle, that contain relation, pattern and pattern id
    return extracted pattern's id 
    """

    # if no verb in this sentence, return null list
    if usePos:
        if sum(map(lambda x:1 if x[1][:2] == "VB" else 0,tokens)) == 0:
            return []

    patternFound = []

    possiblePath = {}
    pathCount = 0


    # visit all words/pos , match pattern
    index = 0
    for word, pos in tokens:
        tagName = getNaivePOSTagName(pos)

        addBecauseWord = -1
        addBecausePOS  = -1

        if word in model:
            addBecauseWord = pathCount
            possiblePath[pathCount] = {"path":model,"start":index}
            pathCount += 1
        if tagName in model:
            addBecausePOS = pathCount
            possiblePath[pathCount] = {"path":model,"start":index}
            pathCount += 1

        needAppend = []
        needRemove = []
        for pathId in possiblePath:
            pathRest = possiblePath[pathId]["path"]
            startFrom = possiblePath[pathId]["start"]

            # find the anwser
            if "_id_" in pathRest:
                ptnId = pathRest["_id_"]
                patternFound.append({"ptnId":ptnId,"start":startFrom,"to":index,"used":True})

            # travarse path
            if pathId == addBecauseWord:
                # move from root to node (word)
                possiblePath[pathId]["path"] = pathRest[word]
            elif pathId == addBecausePOS:
                # move from root to node (pos)
                possiblePath[pathId]["path"] = pathRest[tagName]
            else:
                # here to decide wheather move to next leaf
                inWord = False
                inTag  = False

                if word in pathRest:
                    inWord = True
                    possiblePath[pathId]["path"] = pathRest[word]

                if tagName in pathRest:
                    inTag = True
                    if inWord:
                        # here need to create a new path
                        needAppend.append((pathCount,pathRest[tagName],startFrom))
                        pathCount += 1
                    else:
                        possiblePath[pathId]["path"] = pathRest[tagName]

                if not inWord and not inTag:
                    needRemove.append(pathId)
        
        for pathId in needRemove:
            possiblePath.pop(pathId)
        for pathId,path,start in needAppend:
            possiblePath[pathId] = {"path":path,"start":start}

        index += 1

    # deal with the index
    patternFound = sorted(patternFound,key=lambda x:x["start"])
    for i in range(0,len(patternFound)):
        prevPtn = patternFound[i]
        if prevPtn["used"] == False:
            continue

        for j in range(i+1,len(patternFound)):
            afterPtn = patternFound[j]

            if afterPtn["start"] > prevPtn["to"]:
                break
            else:
                # give up the shorter pattern
                if ( afterPtn["to"] - afterPtn["start"] ) > ( prevPtn["to"] - prevPtn["start"] ):
                    prevPtn["used"] = False
                    break
                else:
                    afterPtn["used"] = False

    result = []
    for ptn in patternFound:
        if ptn["used"]:
            result.append((ptn["ptnId"],ptn["start"],ptn["to"]))

    return result

def getYagoRelation():
    return yagoRelations

def getYagoRelationDomainRange():
    return yagoDomainRange

def getDBPediaRelation():
    return dbpediaRelations

def buildYagoProperties(schema):
    properties = {}
    for relation in getYagoRelation():
        properties[relation] = copy.deepcopy(schema)
    return properties

def buildDBPediaProperties(schema):
    properties = {}
    for relation in getDBPediaRelation():
        properties[relation] = copy.deepcopy(schema)
    return properties

def getSortedStatistic(propertyStatistic):
    properties = {}
    for relation in propertyStatistic:
        # [ (ptnid, {}), (ptnid, {}) ... ]
        properties[relation] = sorted(propertyStatistic[relation].items(),key=lambda x:float(x[1]["support"])/float(x[1]["total"]),reverse=True)
    return properties
        
def getSortedPatternStatistic(propertyStatistic):
    ptnTable = {}

    # build ptnTable[ptnId] = [ (relation, {}), (relation, {}) ... ]
    for relation in propertyStatistic:
        for ptnId in propertyStatistic[relation]:
            ptnS = propertyStatistic[relation][ptnId]
            if not ptnId in ptnTable:
                ptnTable[ptnId] = []
            ptnTable[ptnId].append((relation,ptnS))

    # sort the result
    for ptnId in ptnTable:
        relaList = ptnTable[ptnId]
        if len(relaList) > 1:
            relaList.sort(key=lambda x: x[1]["support"],reverse=True)


    return ptnTable

def getNamedEntityTokens(namedEntity):
    return namedEntity.replace("(","").replace(")","").replace(",","").replace("[","").replace("]","").replace("!","").replace("?","").replace("&","").replace("-","").replace("The","").replace("And","").replace("and","").replace("the","").replace(";","").replace("'s","").replace("\"","").replace("of","").split("_")

def getTokens(string):
    return string.lower().replace("("," ").replace(")"," ").replace(","," ").replace("["," ").replace("]"," ").replace("!"," ").replace("?"," ").replace("&"," ").replace("-"," ").replace("{"," ").replace("}"," ").replace(";"," ").replace("\""," ").replace("'"," ").split("_")

def isPatternValidate(ptnId,table,confidence=-1.0,st=None):
    """isPatternValidate
    檢查此一 pattern 是否可以在接下來的程序之中被使用。
    ptnId: Pattern's id (string)
    table: Pattern table
    confidence: using confidence if confidence >= 0
    """

    # not in table
    if not ptnId in table:
        return False

    # not in `training set'
    if not st == None and not ptnId in st:
        return False

    # FIXME - some old table has no "used"
    if not table[ptnId]["used"]:
        return False
    if "eval" in table[ptnId] and not table[ptnId]["eval"]:
        return False

    # XXX/TODO - ignore too short pattern (it's too general)
    if len(table[ptnId]["pattern"].split()) < 2:
        return False

    # check confidence
    if confidence >= 0 and table[ptnId]["confidence"] < confidence:
        return False

    return True

def checkPath(path):
    """checkPath
    if the path is not a dir, then mkdir it 
    """
    if not os.path.isdir(path):
        os.mkdir(path)

#
#   Classes
#
class naiveNLTKTokenizer(nltk.tokenize.api.TokenizerI):
    """naiveNLTKTokenizer
    privent using nltk's tokenizer, just for speed up.
    """
    def tokenize(self,s):
        """naiveTokenizer - tokenize
        Consider that [\d+] removed by sent into this function
        return the splited string.
        """
        return s.split()

    def span_tokenize(self,s):
        """naiveTokenizer - span_tokenize
        """
        for span in s.split():
            yield span


