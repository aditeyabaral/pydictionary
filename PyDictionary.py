#! env/bin/python
from nltk.corpus import wordnet
import enchant
import argparse
dictionary = enchant.Dict("en_GB")

#command line interface
parser = argparse.ArgumentParser(description='English offline dictionary', usage='PyDictionary word-to-search')
parser.add_argument('word', type=str, help='Search word')
args = parser.parse_args()
word = args.word.strip()
#check = dictionary.check(word)

while not dictionary.check(word):
    otherwords = dictionary.suggest(word)
    if len(otherwords) == 0:
        print("Word not found in dictionary.")
        choice = input("Would you like to add it to the dictionary? ")
        if choice.upper() == 'YES':
            dictionary.add_to_pwl(word)
    else:
        print("Did you mean \"" +otherwords[0]+'\" ?')
    word = input("Enter word to search : ").strip()

syn = wordnet.synsets(word)
dform  = {'n':'noun','v':'verb','a':'adjective','r':'adverb','s':'adjective satellite'}
ctr1 = 1
ctr2 = 97
for i in syn:
    ctr2 = 97
    definition, examples,form = i.definition(), i.examples(),i.pos()
    print(str(ctr1)+'.',end = "")
    print(dform[form], '-', word)
    print("Definition :", definition.capitalize()+'.')
    ctr1+=1
    if len(examples)>0:
        print("Usage : ")
        for j in examples:
            print (chr(ctr2)+'.',j.capitalize()+'.')
            ctr2+=1
    print()
antonyms = []
for i in syn:
    for j in i.lemmas():
        try:
            antonyms.append(j.antonyms()[0].name())
        except:
            pass
if len(antonyms)>0:
    print("Antonyms : ")
    for i in antonyms:
        print(i,end = ",")
