# -*- coding: utf-8 -*-
"""
projizz by qcl
2014.05.17

The python library for operation Projizz.
Add this to the $PYTHON_PATH.


"""
import nltk
import simplejson as json

from textblob import TextBlob


# Combined Files
def combinedFileReader(filename):
    """
    combinedFileReader
    return {"sub-filename":[content of file]}
    """
    f = open(filename,"r")
    articles = json.load(f)
    f.close()
    return articles

def articleSimpleLineFileter(article):
    """
    articleSimpleLineFileter
    input: article (list of lines)
    output: filtered article (list of lines)
    """
    for line in article:
        print line


def naiveTokenizer():
    pass
