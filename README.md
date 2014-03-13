Projizz I/O
-----------
Preprocess for KBA - filter target attributes/properties rapidly.

# Motivation
Linguistic knowledge --> world knowledge

* World knowledge varies with time
* How to acquire knowledge from heterogeneous resources to reflect the changes of real wrold is very important ([KBA](http://trec-kba.org/))


# Problem
Given a _target entity_ to be tracked, find its _(new)_ _related_ _information_ from heterogeneous resources *effectively* because large volume of data are created.

* Target entity 
    * Different patterns related to the entity type
    * e.g. 歐巴馬 - person type 
    * extract all patterns related to person
    * e.g. MS - org type
    * extract pattern related to org.
* Patterns 分類
    * Entites (entities types)
    * Dynamic v.s Static
    * Related information
        * related to some pattern
    * Exact 
        * disambiguation
* Evaluation matrics
    * Speed
        * wiki
        * dbpedia
    * acc, prec, recall
    * TREC KBA  -> to read KBA for more information.
    * Testing Dataset

## Issues
###Target
Target entities have different types, different types have different patterns, different patterns related to differnet types. 

Note that
* Type
* Pattern
* Feature
* Information


1. Information related to human
    * How many features are related to human ?
    * What kinds of features are related to human ?
    * What kinds of patterns can be used to find the features ?
2. Tell out Dynamic and Static information
    * What kinds of features are dynamic, and what kinds of features are static?
    * In other words, what knowledge is unchanged?
3. Tell out the position of the information
4. Tell out if the information is related to the interesting targets

###Efficiency
* Data sturcture and algorithms
* Filtering: (1) and (2)
* Extract: (3) and (4)
* Efficient Filtering, e.g.
    * birth (n patterns related to birth)
    * occupation change (m patterns related to this move)
* If topic model is suitable:
    * birth is a topic, occupation change is a topic,...

###Effectiveness
* Patterns
    1. entity types
    2. dynamic (new) v.s. static 
    3. related information, related to some patterns
    4. exact information, target entites, mention disambiguation

###Others (暫時沒想到分法)
* Pattern coverage
* Pattern use

###Statistics
* Statistics of samples
* Distribution of features
* Number of features/wiki

* How to sample data from wiki for testing?
* Testing effectiveness and efficient
    * Efficiency: enough documents, number of documents created by human per second, ...

# Schedule

# References
* [Identifying constant and unique relations by using time-series text](http://dl.acm.org/citation.cfm?id=2391044)
* [PATTY: a taxonomy of relational patterns with semantic types](http://dl.acm.org/citation.cfm?id=2391076)
    * http://www.mpi-inf.mpg.de/yago-naga/patty/
    * https://d5gate.ag5.mpi-sb.mpg.de/pattyweb/

# Tools
* MongoDB
* Stanford parser?
* Python
    * [RDFLib](https://github.com/RDFLib/rdflib)

# Dataset (may) Used
* [DBpedia](http://wiki.dbpedia.org/Datasets)
    * [Download](http://wiki.dbpedia.org/Downloads39)
        * DBpedia Ontology
        * Raw Infobox Property
        * Raw Infobox Property Definitions
        * Persondata
* [Wikipedia dump](http://en.wikipedia.org/wiki/Wikipedia:Database_download)
    * [20130304](http://dumps.wikimedia.org/enwiki/20130304/)
        * enwiki-20130304-pages-articles
* [PATTY](http://www.mpi-inf.mpg.de/yago-naga/patty/)
    * [PATTY Online](https://d5gate.ag5.mpi-sb.mpg.de/pattyweb/)
