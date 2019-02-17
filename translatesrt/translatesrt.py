import argparse
import os
import re
from itertools import groupby
from collections import namedtuple
from translator import Translator
from progressbar import ProgressBar

class TranslateSrt:

    def __init__(self):
        pass

    def toLanguage(self):
        return 'fr'

    def formatentry(self,entry):
        number, start_end, content = entry
        return ''.join(list((number, start_end, content, '\n')))

    def outputfilename(self,inputfilename):
        filename, extension = os.path.splitext(inputfilename)
        return filename + '-' + self.toLanguage() + extension

    def writesrt(self,entries, filename):
        xs = [ formatentry(x) for x in entries ]
        outputname = self.outputfilename(filename)
        file = open(outputname, 'w')
        file.writelines(xs)

    def validate(self, entries):
        for x in entries:
            assert len(x) == 3, "valid entry must have exactly 3 elemens:" + str(len(x)) + " : " + str(x)

    def parsesrt(self, filename):
        with open(filename) as f:
             entries = [list(g) for b,g in groupby(f, lambda x: bool(x.strip())) if b]
        parsedentries = []

        for entry in entries:
            number, start_end, *content = entry
            parsed_entry = number, start_end, ''.join(content)
            parsedentries.append(parsed_entry)
        self.validate(parsedentries)
        return parsedentries

    def process(self, filename):
        entries = self.parsesrt(filename)
        size = len(entries)
        translatedentries = []
        progress = ProgressBar()
        progress.update_progress(0)
        translator = Translator('en', self.toLanguage())
        for i, entry in enumerate(entries, start=1):
            progress.update_progress(i/size)
            number, start_end, content = entry
            translatedentry = number, start_end, translator.translate(content)
            translatedentries.append(translatedentry)
        return translatedentries

    def run(self):
        parser = argparse.ArgumentParser(description='Translate a srt file')
        parser.add_argument('filename', metavar='file', type=str,
                    help='sub-file to translate')
        args = parser.parse_args()
        self.writesrt(self.process(args.filename), args.filename)
