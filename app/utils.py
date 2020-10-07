def get_suggestions(word):
    return dictionary.suggest(word)


def web_get_records(word):
    #if not dictionary.check(word):
        #return None
    resp = ""
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
    for i in syn[:10]:
        ctr2 = 97
        definition, examples, form = i.definition(), i.examples(), i.pos()
        resp = resp + str(ctr1) + "." + "\n"
        resp = resp + dform[form] + "-" + word + "\n"
        resp = resp + "Definition : " + definition.capitalize() + "." + "\n"
        ctr1 += 1
        antonyms = []
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