import argparse

from common.subtitle_entry import SubtitleEntry
from common.srtfilehandler import SrtFileHandler

class DelaySrt:
    def __init__(self, milliseconds=0, seconds=0, minutes=0, overwrite=False):
       self.milliseconds = milliseconds
       self.seconds = seconds
       self.minutes = minutes
       self.overwrite = overwrite

    def process(self, filename):
        entries = SrtFileHandler.parsesrt(filename)
        for entry in entries:
            print (entry.start_end)

    def run(self, filename):
        self.process(filename)

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
    parser.add_argument('-o', '--overwrite', action='store_false',
                help='overwrite existing file')
    args = parser.parse_args()
    delaysrt = DelaySrt(args.milliseconds, args.seconds, args.minutes, args.overwrite)
    delaysrt.run(args.filename)
