from nltk.corpus import wordnet
from spellchecker import SpellChecker

dictionary = SpellChecker()


def getWordSuggestions(word):
    candidates = dictionary.candidates(word)
    candidates = [w for w in candidates if wordnet.synsets(w)]
    return candidates


def getRecords(word):
    resp = ""
    syn = wordnet.synsets(word)
    if not syn:
        return None

    dform = {
        "n": "noun",
        "v": "verb",
        "a": "adjective",
        "r": "adverb",
        "s": "adjective satellite",
    }
    ctr1 = 1
    ctr2 = 97
    antonyms = list()
    for i in syn[:10]:
        ctr2 = 97
        definition, examples, form = i.definition(), i.examples(), i.pos()
        resp = resp + str(ctr1) + "." + "\n"
        resp = resp + dform[form] + "-" + word + "\n"
        resp = resp + "Definition : " + definition.capitalize() + "." + "\n"
        ctr1 += 1
        if len(examples) > 0:
            resp = resp + "Usage : " + "\n"
            for j in examples:
                resp = resp + chr(ctr2) + ". " + j.capitalize() + "." + "\n"
                ctr2 += 1
        for j in i.lemmas():
            try:
                antonyms.append(j.antonyms()[0].name())
            except IndexError:
                pass
    if len(antonyms) > 0:
        resp = resp + "Antonyms : " + "\n"
        for i in antonyms:
            resp = resp + i + "\n"
    return resp
