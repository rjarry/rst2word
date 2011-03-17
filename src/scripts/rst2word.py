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
import docutils.readers.standalone
import docutils.parsers.rst
import docutils.core
import docutils.io
import rst2wordlib
from docutils.core import publish_cmdline_to_binary

description = ('Generates Microsoft Word documents from standalone reStructuredText '
               'sources.  ' + docutils.core.default_description)

publish_cmdline_to_binary(reader=docutils.readers.standalone.Reader(), 
                          parser=docutils.parsers.rst.Parser(), 
                          writer=rst2wordlib.Writer(), 
                          enable_exit_status=1, 
                          usage=docutils.core.default_usage, 
                          description=description, 
                          destination_class=docutils.io.NullOutput)
