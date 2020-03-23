from nltk.corpus import wordnet as wn
from operator import itemgetter
import operator


def has_numbers(word):
    return any(char.isdigit() for char in word)

data = {}
data_all_synsets = {}
with open('en_wordlist.txt', 'r') as f:
    wordlist = [line.replace("\n", "") for line in f]

for word in wordlist:
    synsets = wn.synsets(word)
    word_synsets = []
    existing = set()
    if len(word) < 3 or has_numbers(word):
        print('Ignoring:', word)
        data[word] = []
        data_all_synsets[word] = []
        continue

    for synset in synsets:
        lemma = synset.lemmas()[0]
        data_all_synsets[word] = data_all_synsets.get(word, []) + [lemma]
        key = ":".join(lemma.key().split(":")[2])
        if key not in existing:
            existing.add(key)
            word_synsets.append([lemma, lemma.key()])
    data[word] = word_synsets
    if len(word_synsets) < 1:
        data_all_synsets[word] = []

tot = 0
data_length = {k: len(v) for k, v in data.items()}
data_all_synsets_length = {k: len(v) for k, v in data_all_synsets.items()}
data = sorted(data_length.items(), key=operator.itemgetter(1))
data_all_synsets = sorted(
    data_all_synsets_length.items(), key=operator.itemgetter(1))

wordnet_original = open("wordnet_original.txt", 'w')
wordnet_restricted = open("wordnet_restricted.txt", 'w')

wordnet_original.write(
    "\n".join([item[0] + "," + str(item[1]) for item in data]))
wordnet_restricted.write(
    "\n".join([item[0] + "," + str(item[1]) for item in data_all_synsets]))

wordnet_original.close()
wordnet_restricted.close()
