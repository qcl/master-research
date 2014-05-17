"""
projizz by qcl
2014.05.17

The python library for operation Projizz.
Add this to the $PYTHON_PATH.


"""

import simplejson as json

# Combined Files
"""
combinedFileReader

return {"sub-filename":[content of file]}
"""
def combinedFileReader(filename):
    f = open(filename,"r")
    articles = json.load(f)
    f.close()
    return articles

