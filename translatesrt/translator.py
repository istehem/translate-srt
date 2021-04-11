import requests
import json
import re
import urllib
from random import randrange
from .language import Language


class Translator:
    def __init__(self, f = Language.FR, t = Language.EN):
        self.from_language = f
        self.to_language = t

    def translate(self, text):
        text = text.replace('\n', '')
        baseurl = 'https://translate.google.com'
        resp = requests.get(baseurl)

        data = {
            'rpcids': 'MkEWBc',
            'f.sid': self.extract('FdrFJe', resp.text),
            'bl': self.extract('cfb2h', resp.text),
            'hl': 'en-US',
            'soc-app': 1,
            'soc-platform': 1,
            'soc-device': 1,
            '_reqid': 1000 + randrange(9000),
            'rt': 'c'
        };

        url = baseurl + '/_/TranslateWebserverUi/data/batchexecute?' + urllib.parse.urlencode(data)
        headers = { 'content-type' : 'application/x-www-form-urlencoded;charset=UTF-8' }
        payload = {
                'f.req' : [[["MkEWBc",f'[["{text}","{self.from_language}","{self.to_language}",true],[null]]','null','generic']]]
                }
        data = urllib.parse.urlencode(payload)
        resp = requests.post(url, data=data, headers=headers)

        # Remove leading junk characters
        content = resp.text[6:]
        p = re.compile(r'\d+')
        length = p.search(content).group()
        content = content[len(length) : int(length) + len(length)]
        xs = json.loads(content)
        xs = json.loads(xs[0][2])

        result = None

        for translation in xs[1][0][0][5]:
            if translation[0]:
                result = translation[0]
                break

        if not result:
            raise LookupError(f'translation for {text} not found in reponse')
        return result

    def extractSid(self, res):
        pass

    def extract(self, key, res):
        regexp = f'"{key}":"(.*?)"'
        p = re.compile(regexp)
        m = p.search(res)
        if not m or not m.group(1):
            raise LookupError(f'key {key} not found in reponse')
        return m.group(1)


if __name__ == '__main__':
    translator = Translator(Language.FR, Language.EN)
    print(translator.translate("Piper, sois plus discrète."))

