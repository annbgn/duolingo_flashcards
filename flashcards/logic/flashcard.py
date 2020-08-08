import datetime
from translate import Translator
from gtts import gTTS
from .duo import duo


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
        for i in raw:
            self.flashcards.append(
                Flashcard(i, self.target_lang, self.known_lang, translator)
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
    def __init__(self, entry, target_lang, known_lang, translator):
        self.target_lang = target_lang
        self.known_lang = known_lang # probably unused. todo: optimize
        self.front = entry.get("word_string")
        start = datetime.datetime.now()
        self.back = translator.translate(self.front)
        print(self.front, " ", self.back)
        end = datetime.datetime.now() - start
        print(end)
        start = datetime.datetime.now()
        try:
            tts = gTTS(text=self.back, lang=target_lang, slow=False)
        except AssertionError:
            self.audio_url = ''
        else:
            self.audio_url = tts.get_urls()
        end = datetime.datetime.now() - start
        print(end)

    def __str__(self):
        return "Flashcard({}, {})".format(self.front, self.back)

    def __repr__(self):
        return "Flashcard({}, {})".format(self.front, self.back)


deck = Deck()
