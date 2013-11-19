Projizz I/O Pre-process
-----------------------

# Schedule
* 2013/11/13 - Dump Wikipedia (English)
    * http://en.wikipedia.org/wiki/Wikipedia:Database_download
    * http://dumps.wikimedia.org/enwiki/latest/
        * enwiki-latest-pages-articles
        * on QCLab (~50G, xml format)
* 2013/11/19 - Distribute to machines

# Plan
- :white_check_mark: Dump/Download
- Preprocess - parse/extract the articles we want
    - need a xml parser
    - :white_check_mark: distribute to linux\* or nlg\* server (人工Map-Reduce)
