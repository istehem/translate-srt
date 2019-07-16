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

    def __init__(self, fromLang, toLang, refreshdb = False):
        self.fromLang = fromLang
        self.toLang = toLang
        self.refreshdb = refreshdb

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

    def run(self, filename):
        self.writesrt(self.process(filename), filename)

