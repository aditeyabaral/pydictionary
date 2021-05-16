import sys
from nltk.corpus import wordnet
from spellchecker import SpellChecker

dictionary = SpellChecker()


def getWordCLI():
    try:
        return sys.argv[1]
    except IndexError:
        print("ERROR: Bad input. You must provide a word!")
        print("Correct usage: \033[1m python3 pyDictionary.py <word> \033[0m")
        sys.exit(2)


def checkWord(word):
    """
    Check if word exist in dictionary

    If not it will try to make suggestions.
    """
    if bool(wordnet.synsets(word)):
        return word

    print("Word not found in dictionary.")
    candidates = dictionary.candidates(word)
    candidates = [w for w in candidates if wordnet.synsets(w)]
    if candidates:
        print(
            f"Did you mean {candidates[0]}?\nOther possibilities include {candidates[1:]}")
        new_word = input("Enter word: ")
        return checkWord(new_word)
    else:
        print("Word not found.")
        sys.exit(2)


def getRecords(word):
    """Search a word in dictionary and print its coincidences"""
    word = checkWord(word)
    syn = wordnet.synsets(word)
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
    for i in syn[:5]:
        ctr2 = 97
        definition, examples, form = i.definition(), i.examples(), i.pos()
        print(str(ctr1) + ". ", end="")
        print(dform[form], "-", word)
        print("Definition:", definition.capitalize() + ".")
        ctr1 += 1
        if len(examples) > 0:
            print("Usage: ")
            for j in examples:
                print(chr(ctr2) + ".", j.capitalize() + ".")
                ctr2 += 1
        print()
        for j in i.lemmas():
            try:
                antonyms.append(j.antonyms()[0].name())
            except IndexError:
                pass
    if len(antonyms) > 0:
        print("Antonyms : ")
        print(",".join(antonyms))


if __name__ == "__main__":
    word = getWordCLI()
    getRecords(word)
