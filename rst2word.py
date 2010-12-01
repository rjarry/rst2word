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

from docutils.core import default_description, default_usage
from docutils.parsers import rst
from docutils.readers import standalone
from docutils.io import NullOutput
import rst2word


description = ('Generates Microsoft Word documents from standalone reStructuredText '
               'sources.  ' + default_description)

def publish_word():
    pub = Publisher(reader=standalone.Reader, 
                    parser=rst.Parser, 
                    writer=rst2word.Writer,
                    destination_class=NullOutput)
    output = pub.publish(usage=default_usage, 
                         description=description, 
                         enable_exit_status=1)
    return output

if __name__ == "__main__":
    publish_word()

