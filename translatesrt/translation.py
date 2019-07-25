from  persistent import Persistent
from .language import Language

class Translation(Persistent):
    def __init__(self, fromLanguage, originalText):
        self.fromLanguage = fromLanguage
        self.originalText = originalText
        self.translations = dict()

