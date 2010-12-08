'''
This file is part of rst2word

Created on 6 dec. 2010
@author: Robin Jarry
'''

from docutils.parsers.rst.directives import misc
from docutils import nodes

class WordDirective(misc.Raw):
    required_arguments = 1
    optional_arguments = 0
    option_spec = {}
    final_argument_whitespace = True
    has_content = False
    
    def run(self):
        command = self.arguments[0]
        attributes = { "format" : "word" }
        node = word('', command, **attributes)
        return [node]


class word(nodes.raw):
    pass