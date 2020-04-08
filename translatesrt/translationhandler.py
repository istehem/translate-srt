import ZODB, ZODB.FileStorage
from collections import namedtuple
from os import path
import transaction

from .language import Language
from .translation import Translation
from .translator import Translator

TranslationKey = namedtuple('TranslationKey', ['language', 'text'])

class TranslationHandler(Translator):
    def __init__(self, f = Language.FR, t = Language.EN, refreshdb=False):
        databasefile = path.join(path.dirname(path.realpath(__file__)), 'translations.fs')
        self.storage = ZODB.FileStorage.FileStorage(databasefile)
        self.db = ZODB.DB(self.storage)
        self.connection = self.db.open()
        self.root = self.connection.root()
        self.memory_connection = ZODB.connection(None)
        self.toLang = t
        self.fromLang = f
        self.refreshdb = refreshdb
        super().__init__(f, t)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.db.close()

    def translate(self, text):
        if not text:
            return text
        translationEntry = None
        key = TranslationKey(language = self.fromLang, text = text)
        if(key in self.root):
            translationEntry = self.root[key]
            translations = translationEntry.translations
            translation = translations.get(self.toLang)
            if not self.refreshdb and translation:
                return translation
            translations[self.toLang] = super().translate(text)
            translationEntry.translations = translations
        else:
            translationEntry = self.createNewTranslationEntry(text)
        assert translationEntry.translations[self.toLang], 'translation missing for: \"{}\"'.format(text)
        self.root[key] = translationEntry
        transaction.commit()
        return translationEntry.translations[self.toLang]

    def createNewTranslationEntry(self, text):
        translationEntry = Translation(self.fromLang, text)
        translationEntry.translations[self.toLang] = super().translate(text)
        return translationEntry

