# -*- coding: utf-8 -*-
"""
projizz by qcl
create: 2014.05.17
modify: 2014.07.04

The python library for operation Projizz.
Add this to the $PYTHONPATH.
"""
#
#   Imports
#
import os
import re
import nltk
import math
import copy
import simplejson as json

from datetime import datetime
from itertools import chain

from .yago import relations as yagoRelations
from .dbpedia import relations as dbpediaRelations
from .yagoRelation import yagoDomainRange

from textblob import TextBlob
from textblob_aptagger import PerceptronTagger

from nltk.corpus import stopwords
from nltk.stem import *
#
#   Variables
#
__author__ = "Qing-Cheng Li <qc.linux@gmail.com>"
__version__ = "0.1"

_removeRefWords = re.compile(r"\[\d+\]") 
_naiveSentenceSpliter = re.compile(r"\.\s+|\!\s+|\?\s+")

_posTagger = PerceptronTagger()

_stopwords = stopwords.words("english")

_stemmer = PorterStemmer()

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
    return namedEntity.replace("(","").replace(")","").replace(",","").replace("[","").replace("]","").replace("!","").replace("?","").replace("&","").replace("-","").replace("The","").replace("And","").replace("and","").replace("the","").replace(";","").replace("'s","").replace("\"","").replace("of","").replace(".","").split("_")

def getTokens(string):
    return string.lower().replace("("," ").replace(")"," ").replace(","," ").replace("["," ").replace("]"," ").replace("!"," ").replace("?"," ").replace("&"," ").replace("-"," ").replace("{"," ").replace("}"," ").replace(";"," ").replace("\""," ").replace("'"," ").replace("."," ").split()

def getTokensWithoutNumbers(string):
    return filter(lambda x: False if "1" in x or "2" in x or "3" in x or "4" in x or "5" in x or "6" in x or "7" in x or "7" in x or "8" in x or "9" in x else True,getTokens(string))

def getStemedTokens(string):
    return list(set(_stemmer.stem(word) for word in getTokens(string) ))

def getStemedTokensWithoutNumbers(string):
    return filter(lambda x: False if "1" in x or "2" in x or "3" in x or "4" in x or "5" in x or "6" in x or "7" in x or "7" in x or "8" in x or "9" in x else True,getStemedTokens(string))

# TODO
def naiveRemovePateernInLine(ptnText,string):
    ptntks = ptnText.split()



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

def getVSMmodels(vsmPath):
    """getVSMmodels
    init the Vector Space Model
    """
    idf = jsonRead(os.path.join(vsmPath,"idf.idf"))
    docs = {}
    lens = {}

    for filename in os.listdir(vsmPath):
        if ".json" in filename:
            rela = filename[:-5]
            docs[rela] = jsonRead(os.path.join(vsmPath,filename))
            
            lens[rela] = getDictVectorLen(docs[rela])
 
    return idf, docs, lens

def getDictVectorLen(d):
    s = 0.0
    for v in d:
        s += (d[v]*d[v])
    return math.sqrt(s)

def cosineSimilarity(v,w,vl=None,wl=None):
    """cosineSimilarity
    return the similarity bewteen dict(v) and dict(w), vl and wl is the length of v and w
    """
    if vl == None:
        vl = getDictVectorLen(v)
    if wl == None:
        wl = getDictVectorLen(w)

    if vl*wl <= 0.0:
        return 0.0

    inner = 0.0
    for word in v:
        if word in w:
            inner += (v[word]*w[word])

    #print v,vl,wl,inner

    return inner/(vl*wl)

def vsmSimilarity(string, models, relas=None, ptntext=None):
    """vsmSimilarity
    input: a string and (idf,docs,lens)
    """
    idf = models[0]
    docs = models[1]
    lens = models[2]

    result = {} 
   
    # Prepare remove ptn words
    ptnw = []
    if not ptntext == None:
        for w in ptntext.split():
            if "[[" not in w:
                t = _stemmer.stem(w)
                if not t in ptnw:
                    ptnw.append(t)

    tv = {}
    tokens = getTokens(string)
    for token in tokens:
        t = _stemmer.stem(token)
        if t not in idf:    # NOTE stopwords will not in idf
            continue
        if t in ptnw:   # remove ptn words
            continue
        if t not in tv:
            tv[t] = 0
        tv[t] += 1

    maxTF = 0
    for w in tv:
        if tv[w] > maxTF:
            maxTF = tv[w]

    for w in tv:
        tv[w] = (float(tv[w])/float(maxTF))*idf[w]

    if relas == None:
        for rela in docs:
            if rela == "produced":
                continue
            sim = cosineSimilarity(tv,docs[rela],wl=lens[rela])
            result[rela] = sim
    else:
        for rela in relas:
            if rela not in docs:
                continue
            sim = cosineSimilarity(tv,docs[rela],wl=lens[rela])
            result[rela] = sim

    return result

def getNBClassifiers(classifierModelPath):
    
    classifiers = {}

    for relation in getYagoRelation():
        if relation == "produced":
            classifiers[relation] = None
            continue

        nbcFilename = os.path.join(classifierModelPath,"%s.nbc" % (relation))
        if os.path.exists(nbcFilename):
            classifiers[relation] = NaiveBayesClassifier()
            classifiers[relation].load(nbcFilename)
        else:
            classifiers[relation] = None

    return classifiers

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

#
class NaiveBayesClassifier(object):
    """Naive Bayes Classifier
    Implement the algorithm @ http://nlp.stanford.edu/IR-book/html/htmledition/naive-bayes-text-classification-1.html
    """
    
    debug = False
    wordList = None
    prior = None
    condprob = None
    tokenize = None

    def _tokenize(self, words):
        if isinstance(words,basestring):
            return getTokens(words)
        else:
            return (w for w in words)

    def debugMsg(self,string):
        if self.debug:
            print string

    def __init__(self,trainData=None,tokenizer=None):
        
        debugMsg = self.debugMsg

        debugMsg("Projizz NaiveBayesClassifer Initialize")

        if tokenizer == None:
            self.tokenize = self._tokenize
        else:
            self.tokenize = tokenizer
        
        if trainData == None:
            return

        ### Initialize
        self.prior = {}
        self.condprob = {}

        countTokensOfTerm = {}
        countDocsInClass = {}

        ### training
        debugMsg("Start Training")
        _startTime = datetime.now() 
        # V <- ExtractVocabulary(D)
        self.wordList = list(set(chain.from_iterable( self.tokenize(words) for words, _ in trainData)))
        debugMsg("Build V, # tokens = %d" % (len(self.wordList)))

        # D <- CountDocs(D)
        N = len(trainData)
        debugMsg("Training size = %d" % (N))

        # get all types
        types = list(set(map(lambda x:x[1], trainData)))
        debugMsg("Types = %s" % (types))

        for words, c in trainData:
            if c not in countDocsInClass:
                countDocsInClass[c] = 0
                countTokensOfTerm[c] = {}

            # CountDocInClass(D,c)
            countDocsInClass[c] += 1
            
            tokens = self._tokenize(words)
            for token in tokens:
                if token not in countTokensOfTerm[c]:
                    countTokensOfTerm[c][token] = 0
                # countTokensOfTerm(text_c,t)
                countTokensOfTerm[c][token] += 1

        debugMsg("Done countDocsInClass, countTokensOfTerm")

        for c in types:
            self.prior[c] = float(countDocsInClass[c])/float(N)

            #print c,sum(map(lambda x:countTokensOfTerm[c][x],countTokensOfTerm[c]))
            #print c,len(self.wordList)

            sum_t_ct = float( sum( map( lambda x:countTokensOfTerm[c][x],countTokensOfTerm[c]) ) + len(self.wordList) )

            for token in self.wordList:
                if token not in self.condprob:
                    self.condprob[token] = {}
                    for _c in types:
                        self.condprob[token][_c] = 0

                t_ct = 0
                if c in countTokensOfTerm and token in countTokensOfTerm[c]:
                    t_ct = countTokensOfTerm[c][token]
                self.condprob[token][c] = float(t_ct+1)/sum_t_ct

        _diff = datetime.now() - _startTime
        debugMsg("Done prior, condprob")
        debugMsg("Done Training in %d.%d seconds" % (_diff.seconds, _diff.microseconds))

    def save(self,modelPath):
        jsonWrite(( self.prior, self.condprob),modelPath)

    def load(self,modelPath):
        self.prior, self.condprob = jsonRead(modelPath)

    def classify(self,document):
        w = self.tokenize(document)
        score = {}
        
        for c in self.prior:
            score[c] = math.log10(self.prior[c])
            #score[c] = self.prior[c]
        
        for t in w:
            if t in self.condprob:  # this may cost many time!
                tc = self.condprob[t]
                for c in score:
                    score[c] += math.log10(tc[c])
                    #score[c] = score[c] * tc[c]
        
        sortedScore = sorted(score.items(), key=lambda x:x[1], reverse=True)
        #for i in sortedScore:
        #    print i,math.pow(10, i[1])
        return sortedScore[0][0]

    def test(self,documents):
        acc = 0
        n = len(documents)
        for words, _c in documents:
            c = self.classify(words)
            if c == _c:
                acc += 1
        return float(acc)/float(n)

