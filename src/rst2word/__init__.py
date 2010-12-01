'''
This file is part of docutils

Created on 21 oct. 2010
@author: Robin Jarry
'''

__docformat__ = 'reStructuredText'

from docutils import writers
from docutils.transforms import writer_aux
from rst2word.visitor import WordTranslator

class Writer(writers.Writer):

    settings_spec = (
        'Microsoft Word Specific Options',
        None,
        (
            ('Specify the template file', ['--word-template'],
                {'default': None, 'metavar': '<file>'}),
            ('Show Word GUI', ['--show-gui'],
                {'default': False, 'action': 'store_true'}),
            ('Auto insert caption titles', ['--auto-caption'],
                {'default': False, 'action': 'store_true'}),
            ('Global scale for all images', ['--image-scale'],
                {'default': 100}),
            
        )
    )


    def __init__(self):
        writers.Writer.__init__(self)
        self.translator_class = WordTranslator

    def get_transforms(self):
        return writers.Writer.get_transforms(self) + [writer_aux.Admonitions]

    def translate(self):
        self.visitor = self.translator_class(self.document)
        try:
            self.document.walkabout(self.visitor)
        finally:
            self.visitor.word.show()

