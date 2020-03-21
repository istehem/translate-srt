import argparse
import os

from common.subtitle_entry import SubtitleEntry
from common.srtfilehandler import SrtFileHandler
from common.time import Time

class DelaySrt:
    def __init__(self, milliseconds=0, seconds=0, minutes=0, overwrite=False):
        self.diff = Time(0, minutes, seconds, milliseconds)
        self.overwrite = overwrite

    def process(self, filename):
        entries = []
        for entry in SrtFileHandler.parsesrt(filename):
            entry.start_end.add(self.diff)
            entries.append(entry)
        return entries

    def outputfilename(self,inputfilename):
        if not self.overwrite:
            filename, extension = os.path.splitext(inputfilename)
            return filename + '-' + 'offset' + extension
        else:
            return inputfilename

    def run(self, filename):
        SrtFileHandler.writesrt(self.process(filename), self.outputfilename(filename))

def main():
    parser = argparse.ArgumentParser(description='Add delay to a srt file')
    parser.add_argument('filename', metavar='file', type=str,
                help='sub-file to apply delay to')
    parser.add_argument('-s', '--seconds', type=int, default=0,
               help='may be negative')
    parser.add_argument('-m', '--minutes', type=int, default=0,
               help='may be negative')
    parser.add_argument('-ms', '--milliseconds', type=int, default=0,
               help='may be negative')
    parser.add_argument('-o', '--overwrite', action='store_true',
                help='overwrite existing file')
    args = parser.parse_args()
    delaysrt = DelaySrt(args.milliseconds, args.seconds, args.minutes, args.overwrite)
    delaysrt.run(args.filename)
