from os import path
import ZODB, ZODB.FileStorage
import random
from pathlib import PurePath
import sys
from collections import namedtuple
import transaction

import urwid
import copy
import argparse
import gettext

from common.utils import projectroot
from common.language import Language

from browsesrt.languageaction import LanguageAction
from browsesrt.filterablelistwalker import FilterableListWalker

class BrowseSrt:

    def __init__(self):
        self.main = urwid.Padding(self.layout(), left=2, right=2)
        urwid.MainLoop(self.main, palette=[('reversed', 'standout', '')], unhandled_input=self.exit_on_q).run()

    def layout(self):
        listbox = self.menu(self.get_keys())
        return urwid.Frame(listbox,
                urwid.Pile([
                    urwid.Text([_('Translation Entries:'), ' ', self.db_filename()]),
                    urwid.Divider(div_char='_'),
                    urwid.Text(['\n'])]))

    def db_filename(self):
        databasefile = path.join(projectroot(), 'db', 'translations.fs')
        return databasefile

    def configure_db(self):
        storage = ZODB.FileStorage.FileStorage(self.db_filename())
        self.db = ZODB.DB(storage)

    def format_key(self, k):
        return f'{k.language}: {k.text}'

    def exit_on_q(self, key):
        if key in ('q', 'Q'):
            raise urwid.ExitMainLoop()

    def get_keys(self):
        try:
            self.configure_db()
            connection = self.db.open()
            root = connection.root()
            memory_connection = ZODB.connection(None)
            return root.keys()

        except Exception as e:
            print(e)
        finally:
            self.db.close()

        return []

    def get_translations(self, key):
        self.configure_db()
        try:
            connection = self.db.open()
            root = connection.root()
            memory_connection = ZODB.connection(None)
            if key in root:
                return root[key].translations
        except Exception as e:
            self.db.close()
            raise e
        finally:
            self.db.close()
        return []

    def item_chosen(self, button, key):
        main_menu = copy.copy(self.main.original_widget)
        translations = self.get_translations(key)
        responses = [urwid.Text([self.format_key(key)])]
        for l, t in translations.items():
            response = urwid.Text([f'{str(l)} : {str(t)}', '\n'])
            responses.append(response)

        done = urwid.Button(_('Back'))
        responses.append(urwid.AttrMap(done, None, focus_map='reversed'))
        urwid.connect_signal(done, 'click', self.set_current_widget, main_menu)
        self.main.original_widget = urwid.Filler(urwid.Pile(responses))

    def set_current_widget(self, button, widget):
        self.main.original_widget = widget

    def menu(self, entries):
        body = []
        for e in entries:
            button = urwid.Button(self.format_key(e))
            urwid.connect_signal(button, 'click', self.item_chosen, e)
            body.append(urwid.AttrMap(button, None, focus_map='reversed'))
        return urwid.ListBox(FilterableListWalker(body))

def main():
    i18n = Language.EN
    parser = argparse.ArgumentParser(description='Browse available translatons')
    parser.add_argument('-l', '--use-lang', type=Language, action=LanguageAction,
               help='internationalization and localization, default ({})'.format(i18n), default=i18n)
    args = parser.parse_args()

    language_key = {
            Language.DE : 'de',
            Language.EN : 'en_US'
        }.get(args.use_lang)

    lang = gettext.translation('browsesrt', localedir = path.join(projectroot(), 'browsesrt', 'locales'), languages = [language_key])
    lang.install()
    _ = lang.gettext
    BrowseSrt()
