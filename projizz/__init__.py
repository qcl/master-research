# -*- coding: utf-8 -*-
"""
projizz by qcl
create: 2014.05.17
modify: 2014.05.18

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
        print line.encode("utf-8")

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


