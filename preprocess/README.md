Projizz I/O Pre-process
-----------------------

# Schedule
* 2013/11/13 - Dump Wikipedia (English)
    * http://en.wikipedia.org/wiki/Wikipedia:Database_download
    * http://dumps.wikimedia.org/enwiki/latest/
        * enwiki-latest-pages-articles
        * on QCLab (~50G, xml format)
* 2013/11/19 - Distribute to machines
* 2013/11/20 - 將有{{Infobox P*的文章抽出完成。
* 2013/11/21 - 再分佈，第二次grep

# Plan
- :white_check_mark: Dump/Download
- Preprocess - parse/extract the articles we want
    - :white_check_mark: need a xml parser (1)
    - :white_check_mark: distribute to linux\* or nlg\* server (人工Map-Reduce)
    - :white_check_mark: xml -> 文章/template info
- Patterns Extraction?
