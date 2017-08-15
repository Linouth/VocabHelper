from database import Entry
import requests
import re
from operator import itemgetter


class GlosbeTranslator():
    __api_url = "https://glosbe.com/gapi/translate"

    def __init__(self, from_lang, dest_lang):
        self.from_lang = from_lang
        self.dest_lang = dest_lang

    def translate(self, phrase):
        r = requests.get(self.__api_url, params={
            'from': self.from_lang,
            'dest': self.dest_lang,
            'phrase': phrase,
            'tm': False,
            'format': 'json'
        })
        json = r.json()
        if json['result'] != 'ok':
            return None

        # No results found
        if len(json['tuc']) == 0:
            return None

        # Check if plural, if so fetch propper translation
        patterns = [
                '[Pp]lural form of (\w+)',
                '[Pp]resent participle of (\w+)',
                '[Ss]imple past tense and past participle of (\w+)'
        ]
        for pattern in patterns:
            plural = re.search(pattern, r.text)
            if plural:
                return self.translate(plural.group(1))

        # Prepare and format database entry
        entry = Entry()
        for t in sorted(json['tuc'], key=itemgetter('authors'), reverse=True):
            if t.get('phrase'):
                best = t
                break
        entry.searchstring = phrase
        entry.phrase = best['phrase']['text'].capitalize()
        if best.get('meanings'):
            entry.meaning = best['meanings'][0]['text'].capitalize()

        # Return database entry; NOT SAVED YET
        return entry


if __name__ == '__main__':
    tr = GlosbeTranslator('en', 'nl')
    words = []
    words.append(tr.translate('ulcer'))
    words.append(tr.translate('imperatives'))
