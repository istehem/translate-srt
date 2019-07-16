import argparse
from translatesrt import TranslateSrt
from language import Language

def main():
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
    translatsrt = TranslateSrt(args.from_lang, args.to_lang, args.refresh_db)
    translatsrt.run(args.filename)


if __name__ == '__main__':
    main()
