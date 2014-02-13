Projizz I/O
-----------
Preprocess for KBA - filter target attributes/properties rapidly.

# Problem
Given a _target entity_ to be tracked, find its _(new)_ _related_ _information_ from heterogeneous resources.

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
    * TREC KBA
    * Testing Dataset


# Schedule

# References
* [Identifying constant and unique relations by using time-series text](http://dl.acm.org/citation.cfm?id=2391044)
* [PATTY: a taxonomy of relational patterns with semantic types](http://dl.acm.org/citation.cfm?id=2391076)
    * http://www.mpi-inf.mpg.de/yago-naga/patty/
    * https://d5gate.ag5.mpi-sb.mpg.de/pattyweb/

# Tools
* MongoDB
* Stanford parser?

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
