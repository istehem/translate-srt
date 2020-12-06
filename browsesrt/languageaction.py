from common.language import Language
import argparse

class LanguageAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        supported_languages = [Language.EN, Language.DE]
        if values not in supported_languages:
            supported_langs_str = ', '.join([f'\'{str(x)}\'' for x in supported_languages])
            raise argparse.ArgumentError(self, f'Language \'{str(values)}\' not supported. Supported: {supported_langs_str}')
        setattr(namespace, self.dest, values)
