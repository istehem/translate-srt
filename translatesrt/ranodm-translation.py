from os import path
import ZODB, ZODB.FileStorage
from collections import namedtuple
import random

from translation import Translation
from language import Language

TranslationKey = namedtuple('TranslationKey', ['language', 'text'])

if __name__ == '__main__':
    databasefile = path.join(path.dirname(path.realpath(__file__)), 'translations.fs')
    storage = ZODB.FileStorage.FileStorage(databasefile)
    db = ZODB.DB(storage)

    try:
        connection = db.open()
        root = connection.root()
        memory_connection = ZODB.connection(None)
        translationEntry = root[random.choice(list(root.keys()))]
        translation = translationEntry.translations[Language.EN]
        if translation:
            print('################## Random Translation [{}] ####################'.format(translationEntry.fromLanguage))
            print(translationEntry.originalText)
            print(translation)
        else:
            print('Nothing found today')
    except Exception as e:
        print(e)
    finally:
        db.close()

