import ZODB, ZODB.FileStorage
from language import Language
from translation import Translation
import BTrees.OOBTree
import transaction
from translator import Translator
from collections import namedtuple

TranslationKey = namedtuple('TranslationKey', ['language', 'text'])

class TranslationHandler(Translator):
    def __init__(self, f = Language.FR, t = Language.EN, refreshdb=False):
        self.storage = ZODB.FileStorage.FileStorage('translations.fs')
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
        translatedText = None
        translationEntry = None
        key = TranslationKey(language = self.fromLang, text = text)
        if(key in self.root):
            translationEntry = self.root[key]
            translations = translationEntry.translations
            translation = translations[self.toLang]
            if not self.refreshdb and translation:
                return translation
            translatedText = super().translate(text)
            translations[self.toLang] = translatedText
        else:
            translationEntry = self.createNewTranslationEntry(text)
        assert translationEntry.translations[self.toLang], "translation missing"
        self.root[key] = translationEntry
        transaction.commit()
        return translatedText

    def createNewTranslationEntry(self, text):
        translationEntry = Translation(text)
        translatedText = super().translate(text)
        translationEntry.translations[self.toLang] = translatedText
        return translationEntry

