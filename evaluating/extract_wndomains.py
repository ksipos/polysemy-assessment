import csv
from nltk.corpus import wordnet as wn

with open('wn-domains-3.2/wordnet-3.0-mapping.txt', 'r') as f:
    reader = csv.reader(f, delimiter=' ')
    synsets = {}
    for line in reader:
        wnoffset = line[0].split("-")
        synsetid = wn.synset_from_pos_and_offset(wnoffset[1], int(wnoffset[0])).name()
        labels = line[1:]
        for domain in labels:
            domain = domain.strip().lower()
            synsets[synsetid] = synsets.get(synsetid, []) + [domain]


with open("wndomains_senses.txt", 'w') as f:
    for k, v in synsets.items():
        f.write('"' + k + '" "' + " ".join(v) + '"\n')

with open("pyramid_output2/pca4_L1", 'r') as f:
    words = [line.replace("\n", "").split(",")[0] for line in f]


detected = {}
for word in words:
    word_synsets = wn.synsets(word)
    for synset in word_synsets:
        synset = synset.name()
        if synset in synsets:
            detected[word] = detected.get(word, []) + [synsets[synset]]


with open('wndomains_ranking.txt', 'w') as f:
    for word in words:
        f.write(word + "," + str(len(detected.get(word, []))) + "\n")
