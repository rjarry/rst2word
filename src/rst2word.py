#!C:\tools\python26\python.exe

# $Id: rst2html.py 4564 2006-05-21 20:44:42Z wiemann $
# Author: David Goodger <goodger@python.org>
# Copyright: This module has been placed in the public domain.

"""
A minimal front end to the Docutils Publisher, producing HTML.
"""

try:
    import locale
    locale.setlocale(locale.LC_ALL, '')
except:
    pass
from docutils.readers import standalone
from docutils.parsers import rst
from docutils import core
from docutils.io import NullOutput
import rst2word

description = ('Generates Microsoft Word documents from standalone reStructuredText '
               'sources.  ' + core.default_description)

def publish_word():
    pub = core.Publisher(reader=standalone.Reader(), 
                         parser=rst.Parser(), 
                         writer=rst2word.Writer(), 
                         destination_class=NullOutput)
    output = pub.publish(usage=core.default_usage, 
                         description=description, 
                         enable_exit_status=1)
    return output

if __name__ == "__main__":
    publish_word()

