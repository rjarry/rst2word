'''
This file is part of docutils

Created on 21 oct. 2010
@author: Robin Jarry
'''

__docformat__ = 'reStructuredText'

from docutils import writers
from docutils.transforms import writer_aux
from rst2wordlib.visitor import WordTranslator

class Writer(writers.Writer):

    settings_spec = (
        'Microsoft Word Specific Options',
        None,
        (
            ('Specify the template file', ['--word-template'],
                {'default': None, 'metavar': '<file>'}),
            ('Show Word GUI during document generation (slows down the process)', ['--show-gui'],
                {'default': False, 'action': 'store_true'}),
            ('Auto insert caption titles', ['--auto-caption'],
                {'default': False, 'action': 'store_true'}),
            ('Global scale for all images', ['--image-scale'],
                {'default': 100}),
            ('Table of Contents depth', ['--toc-depth'],
                {'default': 3}),   
            ('Headless mode', ['--headless'],
                {'default': False, 'action': 'store_true'}),
            
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
            self.visitor.word.saveAs(self.visitor.destination)
        finally:
            if self.document.settings.headless:
                self.visitor.word.quit()
            else:
                self.visitor.word.show()

