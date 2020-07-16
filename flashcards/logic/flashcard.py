from .duo import duo
import datetime


class Deck:
    target_lang  = None
    known_lang = 'en'
    flashcards = []

    def fill_deck(self, raw, target_lang, known_lang):
        self.target_lang = target_lang
        self.known_lang = known_lang
        self.flashcards = []
        for i in raw:
            self.flashcards.append(Flashcard(i, self.target_lang, self.known_lang))

    def __str__(self):
        return "Deck({}, {}, {} flashcards)".format(self.target_lang, self.known_lang, len(self.flashcards))

    def __repr__(self):
        return "Deck({}, {}, {} flashcards)".format(self.target_lang, self.known_lang, len(self.flashcards))

    def __iter__(self):
        for fc in self.flashcards:
            yield fc

    def __getitem__(self, index):
        return self.flashcards.__getitem__(index)


class Flashcard:
    def __init__(self, entry, target_lang, known_lang):
        self.target_lang = target_lang
        self.target_lang = known_lang
        self.front = entry.get('word_string')
        normalized_string = entry.get('normalized_string')
        start = datetime.datetime.now()
        self.back = duo.duo.get_translations([normalized_string], source=known_lang, target=target_lang)[normalized_string] or "no data"
        end = datetime.datetime.now() - start
        print(end)
        start = datetime.datetime.now()
        self.audio_url = duo.duo.get_audio_url(self.front, language_abbr=target_lang)
        end = datetime.datetime.now() - start
        print(end)

    def __str__(self):
        return "Flashcard({}, {})".format(self.front, self.back)

    def __repr__(self):
        return "Flashcard({}, {})".format(self.front, self.back)


deck = Deck()
