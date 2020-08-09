import json
import random

import requests
from translate import Translator


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
        response = requests.get("https://www.duolingo.com/api/1/version_info")
        if response.ok:
            try:
                data = json.loads(response.content)
                tts = data["tts_base_url_http"]
                voices = json.loads(data["tts_voice_configuration"]["multi_voices"])[target_lang]
                voices[0]
            except Exception as ಠ_ಠ:
                print(ಠ_ಠ)
                audio_base = None
            else:
                audio_base = tts + "tts/" + random.choice(voices) + "/token"

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
        self.back = translator.translate(self.front)
        print(self.front, " ", self.back)

        self.audio_url = audio_base + "/" + self.front if audio_base else None

    def __str__(self):
        return "Flashcard({}, {})".format(self.front, self.back)

    def __repr__(self):
        return "Flashcard({}, {})".format(self.front, self.back)


deck = Deck()
