import argparse

class DelaySrt:
    def __init__(self, seconds, minutes, overwrite=False):
       self.seconds = seconds
       self.minutes = minutes
       self.overwrite = overwrite

    def run(self, filename):
        pass

def main():
    parser = argparse.ArgumentParser(description='Add delay to a srt file')
    parser.add_argument('filename', metavar='file', type=str,
                    help='sub-file to apply delay to')
    parser.add_argument('-s', '--seconds', type=int,
               help='may be negative')
    parser.add_argument('-m', '--minutes', type=int,
               help='may be negative')
    parser.add_argument('-o', '--overwrite', action='store_false',
                help='overwrite existing file')
    args = parser.parse_args()
    delaysrt = DelaySrt(args.seconds, args.minutes, overwrite)
    translatsrt.run(args.filename)
