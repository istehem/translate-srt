import argparse
import os
import re
from itertools import groupby
from collections import namedtuple

from translator import Translator
from progressbar import ProgressBar
from language import Language
from translationhandler import TranslationHandler


SubtitleEntry = namedtuple('SubtitleEntry', ['number', 'start_end', 'content'])

class TranslateSrt:

    def __init__(self):
        pass

    def formatentry(self,entry):
        return ''.join(list((entry.number, entry.start_end, entry.content, '\n')))

    def outputfilename(self,inputfilename):
        filename, extension = os.path.splitext(inputfilename)
        return filename + '-' + str(self.toLang) + extension

    def writesrt(self,entries, filename):
        xs = [ self.formatentry(x) for x in entries ]
        outputname = self.outputfilename(filename)
        with open(outputname, 'w') as f:
            f.writelines(xs)

    def parsesrt(self, filename):
        with open(filename) as f:
             entries = [list(g) for b,g in groupby(f, lambda x: bool(x.strip())) if b]
        parsedentries = []

        for entry in entries:
            number, start_end, *content = entry
            parsed_entry = SubtitleEntry(number, start_end, ''.join(content))
            parsedentries.append(parsed_entry)
        return parsedentries

    def process(self, filename):
        entries = self.parsesrt(filename)
        size = len(entries)
        translatedentries = []
        progress = ProgressBar()
        progress.update_progress(0)
        with TranslationHandler(self.fromLang, self.toLang, self.refreshdb) as translator:
            for i, entry in enumerate(entries, start=1):
                progress.update_progress(i/size)
                translatedentry = SubtitleEntry(entry.number, entry.start_end, translator.translate(entry.content))
                translatedentries.append(translatedentry)
        return translatedentries

    def run(self):
        parser = argparse.ArgumentParser(description='Translate a srt file')
        parser.add_argument('filename', metavar='file', type=str,
                    help='sub-file to translate')
        parser.add_argument('-f', '--from-lang', type=Language,
                help='language to translate to (en, de, fr ...)', default=Language.FR)
        parser.add_argument('-t', '--to-lang', type=Language,
                help='language to translate to (en, de, fr ...)', default=Language.EN)
        parser.add_argument('-r', '--refresh-db', action='store_true',
                help='override existing database translations')
        args = parser.parse_args()
        self.toLang = args.to_lang
        self.fromLang = args.from_lang
        self.refreshdb = args.refresh_db
        self.writesrt(self.process(args.filename), args.filename)
