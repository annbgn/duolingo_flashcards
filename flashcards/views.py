import random

import duolingo
import ujson
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .logic.duo import duo


def index(request):
    return render(request, "flashcards/index.html")


def _validate_username(username):
    # todo implement check that it's not email
    return username


def _sort(a, b):
    if a.strength > b.srength:
        return a
    return b


@csrf_exempt
def get_login_data_view(request):
    username = _validate_username(request.POST.get("uname", None))
    password = request.POST.get("psw", None)
    # todo: validate

    try:
        duo.duo = duolingo.Duolingo(username, password)
    except Exception as ಠ_ಠ:
        print(ಠ_ಠ)
        # todo: return message or redirect to index

    context = {"langs": duo.duo.get_languages(abbreviations=True)}
    print(context)
    return render(request, "flashcards/select_language.html", context)


@csrf_exempt
def practice(request):
    from .logic.flashcard import deck

    lang = request.POST.get("lang", None)
    vocab_dict = duo.duo.get_vocabulary(language_abbr=lang)
    amount = len(vocab_dict.get("vocab_overview", []))

    target_lang = vocab_dict.get("learning_language")
    known_lang = vocab_dict.get("from_language")
    flashcard_billets = random.sample(
        vocab_dict.get("vocab_overview", []), k=20 if amount > 20 else amount
    )

    deck.fill_deck(flashcard_billets, target_lang, known_lang)
    print(deck)

    data = {
        fc.front: {"back": fc.back, "audio_url": fc.audio_url} for fc in deck.flashcards
    }
    context = {"deck": ujson.dumps(data)}
    print(context)
    return render(request, "flashcards/practice.html", context)
