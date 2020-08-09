import datetime
from translate import Translator
from gtts import gTTS
from .duo import duo
import requests
import json
import random


class Deck:
    target_lang = None
    known_lang = "en"
    flashcards = []

    def fill_deck(self, raw, target_lang, known_lang):
        self.target_lang = target_lang
        self.known_lang = known_lang
        self.flashcards = []
        translator = Translator(
            provider="mymemory", to_lang=known_lang, from_lang=target_lang
        )
        response = requests.get('https://www.duolingo.com/api/1/version_info')
        if response.ok:
            try:
                data = json.loads(response.content)
                tts = data['tts_base_url_http']
                print(tts)
                print(target_lang)
                voices = json.loads(data['tts_voice_configuration']['multi_voices'])[target_lang]
                print(voices)
                voices[0]
            except Exception as ಠ_ಠ:
                print(ಠ_ಠ)
                audio_base = None
            else:
                audio_base = tts + 'tts/' + random.choice(voices) + '/token'
            finally:
                print(audio_base)
        for i in raw:
            self.flashcards.append(
                Flashcard(i, self.target_lang, self.known_lang, translator, audio_base)
            )

    def __str__(self):
        return "Deck({}, {}, {} flashcards)".format(
            self.target_lang, self.known_lang, len(self.flashcards)
        )

    def __repr__(self):
        return "Deck({}, {}, {} flashcards)".format(
            self.target_lang, self.known_lang, len(self.flashcards)
        )

    def __iter__(self):
        for fc in self.flashcards:
            yield fc

    def __getitem__(self, index):
        return self.flashcards.__getitem__(index)


class Flashcard:
    def __init__(self, entry, target_lang, known_lang, translator, audio_base):
        self.target_lang = target_lang
        self.known_lang = known_lang  # probably unused. todo: optimize
        self.front = entry.get("word_string")
        self.id = entry.get("id")  # used for getting audio
        start = datetime.datetime.now()
        self.back = translator.translate(self.front)
        print(self.front, " ", self.back)
        end = datetime.datetime.now() - start

        start = datetime.datetime.now()
        """
        try:
            tts = gTTS(text=self.back, lang=target_lang, slow=False)
            self.audio_url = tts.get_urls()[0]
        except (AssertionError, IndexError):
            self.audio_url = ''
        """
        # self.audio_url =  self.id
        self.audio_url = audio_base + '/' + self.front if audio_base else None
        print(self.audio_url)
        end = datetime.datetime.now() - start

    def __str__(self):
        return "Flashcard({}, {})".format(self.front, self.back)

    def __repr__(self):
        return "Flashcard({}, {})".format(self.front, self.back)


deck = Deck()
