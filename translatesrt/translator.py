import requests
import json
import subprocess
from os import path
from language import Language

class Translator:
    def __init__(self, f = Language.FR, t = Language.EN):
        self.opts = self.getDefaults()
        self.opts['from'] = f
        self.opts['to'] = t

    def translate(self, text):
        return self.sendRequest(text)

    def sendRequest(self, text):
        url = 'https://translate.google.com/translate_a/single'
        data = {
            'client': self.opts['client'],
            'sl': self.opts['from'],
            'tl': self.opts['to'],
            'hl': self.opts['to'],
            'dt': ['at', 'bd', 'ex', 'ld', 'md', 'qca', 'rw', 'rm', 'ss', 't'],
            'ie': 'UTF-8',
            'oe': 'UTF-8',
            'otf': 1,
            'ssel': 0,
            'tsel': 0,
            'kc': 7,
            'q': text
        }
        token = self.getToken(text)
        data[token['name']] = token['value']

        resp = requests.get(url, params=data)
        if resp.status_code != 200:
            raise ValueError('GET error {}'.format(resp.status_code))
        result = ''.join([ x[0] for x in resp.json()[0] if x[0] ])
        return result

    def getDefaults(self):
        return {
            'client' : 't',
            'from' : Language.FR,
            'to' :   Language.EN
        }

    def getToken(self, text):
        tokenscript = path.join(path.dirname(path.realpath(__file__)), 'get-api-token.js')
        t = subprocess.check_output(['node', tokenscript, text])
        return json.loads(t)


if __name__ == '__main__':
    translator = Translator('en', 'fr')
    print(translator.translate("how are you?"))

