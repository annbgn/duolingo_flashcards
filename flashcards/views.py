import datetime
import random

import duolingo
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.views.decorators.csrf import csrf_exempt, csrf_protect

import ujson

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
        start = datetime.datetime.now()
        duo.duo = duolingo.Duolingo(username, password)
        end = datetime.datetime.now() - start
        print(end)
    except Exception as ಠ_ಠ:
        print(ಠ_ಠ)
        # todo: return message or redirect to index

    start = datetime.datetime.now()
    context = {"langs": duo.duo.get_languages(abbreviations=True)}
    end = datetime.datetime.now() - start
    print(end)
    print(context)
    return render(request, "flashcards/select_language.html", context)


@csrf_exempt
def wordlist(request):
    from .logic.flashcard import Deck, deck

    lang = request.POST.get("lang", None)
    # skills = list(map(lambda x: x.get('name', '').lowercase(), duo.duo.get_learned_skills(lang)))
    print('get vocab', end='')
    start = datetime.datetime.now()
    vocab_dict = duo.duo.get_vocabulary(language_abbr=lang)
    end = datetime.datetime.now() - start
    print(end)
    amount = len(vocab_dict.get("vocab_overview", []))
    # sorted(vocab_dict, key=lambda x: x['order'], reverse=True)

    target_lang = vocab_dict.get("learning_language")
    known_lang = vocab_dict.get("from_language")
    flashcard_billets = random.sample(
        vocab_dict.get("vocab_overview", []), k=20 if amount > 20 else amount
    )

    print('fill deck', end='')
    start = datetime.datetime.now()
    deck = deck.fill_deck(flashcard_billets, target_lang, known_lang)
    print(deck)
    end = datetime.datetime.now() - start
    print(end)
    
    context = {"deck": deck}
    return render(request, "flashcards/wordlist.html", context)


@csrf_exempt
def practice(request):
    from .logic.flashcard import Deck, deck

    data = {fc.front: {'back': fc.back, 'audio_url': fc.audio_url} for fc in deck.flashcards}
    context = {"deck": ujson.dumps(data)}
    print(context)
    return render(request, "flashcards/practice.html", context)
