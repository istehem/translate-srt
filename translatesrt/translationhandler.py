import ZODB, ZODB.FileStorage
from language import Language
from translation import Translation
import BTrees.OOBTree
import transaction
from translator import Translator

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
        if(text in self.root):
            translations = self.root[text].translations
            translation = translations[self.toLang]
            if not self.refreshdb and translation:
                return translation
            translatedText = super().translate(text)
            translations[self.toLang] = translatedText
        else:
            translations = Translation(text)
            translatedText = super().translate(text)
            translations.translations[self.toLang] = translatedText
            self.root[text] = translations
        transaction.commit()
        return translatedText


