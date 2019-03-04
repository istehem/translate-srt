from  persistent import Persistent
from language import Language

class Translation(Persistent):
    def __init__(self, original, fromLanguage):
        self.fromLanguage = fromLanguage
        self.original = original
        self.translations = dict()

