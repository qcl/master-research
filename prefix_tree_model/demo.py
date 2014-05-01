# -*- coding: utf-8 -*-
from textblob import TextBlob
from textblob_aptagger import PerceptronTagger
import nltk
import time
import re

string="""Rapid growth since incorporation has triggered a chain of products, acquisitions and partnerships beyond Google's core search engine. It offers online productivity software including email (Gmail), an office suite (Google Drive), and social networking (Google+). Desktop products include applications for web browsing, organizing and editing photos, and instant messaging. The company leads the development of the Android mobile operating system and the browser-only Chrome OS[12] for a netbook known as a Chromebook. Google has moved increasingly into communications hardware: it partners with major electronics manufacturers in production of its high-end Nexus devices and acquired Motorola Mobility in May 2012.[13] In 2012, a fiber-optic infrastructure was installed in Kansas City to facilitate a Google Fiber broadband service.[14]"""

class qcl_tokenizer(nltk.tokenize.api.TokenizerI):
    def tokenize(self,s):
        # FIXME e.g This is a book[1]
        return s.lower().replace("["," ").replace("]"," ").replace("!"," ").replace("?"," ").replace(","," ").replace(")"," ").replace("("," ").replace("\""," ").replace("'"," ").split()
    def span_tokenize(self,s):
        tokened = self.tokenize(s)
        for span in tokened:
            yield span

#tagger = PerceptronTagger()
#tokenize = qcl_tokenizer()

#print "Demo"
#a = TextBlob(string,pos_tagger=tagger)
#print a.tags

#print "Demo2"
#b = TextBlob(string,tokenizer=tokenize,pos_tagger=tagger)
#print b.tokens
#print b.tokens

removeRef = re.compile(r"\[\d+\]")
print removeRef.sub("",string)


