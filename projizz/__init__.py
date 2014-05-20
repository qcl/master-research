# -*- coding: utf-8 -*-
"""
projizz by qcl
create: 2014.05.17
modify: 2014.05.20

The python library for operation Projizz.
Add this to the $PYTHONPATH.
"""
#
#   Imports
#
import re
import nltk
import simplejson as json

from textblob import TextBlob
from textblob_aptagger import PerceptronTagger

#
#   Variables
#
__author__ = "Qing-Cheng Li <qc.linux@gmail.com>"
__version__ = "0.1"

_removeRefWords = re.compile(r"\[\d+\]") 
_naiveSentenceSpliter = re.compile(r"\.\s+|\!\s+|\?\s+")

_posTagger = PerceptronTagger()

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
    for word, pos in tokens:
        tagName = getNaivePOSTagName(pos)

        addBecauseWord = -1
        addBecausePOS  = -1

        if word in model:
            addBecauseWord = pathCount
            possiblePath[pathCount] = model
            pathCount += 1
        if tagName in model:
            addBecausePOS = pathCount
            possiblePath[pathCount] = model
            pathCount += 1

        needAppend = []
        needRemove = []
        for pathId in possiblePath:
            pathRest = possiblePath[pathId]

            # find the anwser
            if "_id_" in pathRest:
                ptnId = pathRest["_id_"]
                if not ptnId in patternFound:
                    patternFound.append(ptnId)

            # travarse path
            if pathId == addBecauseWord:
                # move from root to node (word)
                possiblePath[pathId] = pathRest[word]
            elif pathId == addBecausePOS:
                # move from root to node (pos)
                possiblePath[pathId] = pathRest[tagName]
            else:
                # here to decide wheather move to next leaf
                inWord = False
                inTag  = False

                if word in pathRest:
                    inWord = True
                    possiblePath[pathId] = pathRest[word]

                if tagName in pathRest:
                    inTag = True
                    if inWord:
                        # here need to create a new path
                        needAppend.append((pathCount,pathRest[tagName]))
                        pathCount += 1
                    else:
                        possiblePath[pathId] = pathRest[tagName]

                if not inWord and not inTag:
                    needRemove.append(pathId)
        
        for pathId in needRemove:
            possiblePath.pop(pathId)
        for pathId,path in needAppend:
            possiblePath[pathId] = path

    return patternFound

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


