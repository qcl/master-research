# -*- coding: utf-8 -*-
# qcl
# testing classify

from textblob.classifiers import NaiveBayesClassifier
from itertools import chain
import projizz


def projizz_get_words_from_dataset(dataset):
    """自幹_get_words_from_dataset
    """

    def tokenize(words):
        if isinstance(words, basestring):
            return projizz.getTokens(words)
        else:
            return (w for w in words)

    all_words = chain.from_iterable( tokenize(words) for words, _ in dataset) 
    return set(all_words)

def projizz_extractor(document, train_set):
    """自幹extractor，試圖取代basic_extractor
    """
    #word_features = 

    if isinstance(document, basestring):
        #tokens = 
        pass
    else:
        #tokens = 
        pass


train = [
    ("I love this sandwich.", "pos"),
    ("This is an amazing place!", "pos"),
    ("I feel very good about these beers.", "pos"),
    ("This is my best work.", "pos"),
    ("What an awesome view","pos"),
    ("I do not like this restautant","neg"),
    ("I am tired of this stuff.","neg"),
    ("I can't deal with this","neg"),
    ("He is my sworn enemy!","neg"),
    ("My boss is horrible.","neg")
]

test = [
    ("The beer was good.","pos"),
    ("I do not enjoy my job","neg"),
    ("I ain't feeling dandy today.","neg"),
    ("I feel amazing!","pos"),
    ("Gary is a frienf of mine.","pos"),
    ("I can't believe I'm doing this.","neg")
]

train = [
    ("Chinese Beijing Chinese","yes"),
    ("Chinese Chinese Shanghai","yes"),
    ("Chinese Macao","yes"),
    ("Tokyo Japan Chinese","no")
        ]

test = [
    ("Chinese Chinese Chinese Tokyo Japan","yes")
        ]



#cl = NaiveBayesClassifier(train)
#
#print cl.classify("Their burgers are amazing")
#
#print cl.accuracy(test)

#print projizz_get_words_from_dataset(train)
#print projizz.getStemedTokens("This this is a tt tt test test")

cl2 = projizz.NaiveBayesClassifier(train)

print cl2.classify("Chinese Chinese Chinese Tokyo Japan")
print cl2.classify("Tokyo Japan")
print cl2.classify("Taiwan")
