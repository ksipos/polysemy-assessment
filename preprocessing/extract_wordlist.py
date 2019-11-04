from nltk.corpus import wordnet as wn
from operator import itemgetter 

with open("en_frequency.txt", "r") as f:
    frequent_words = {line.replace("\n", "").split()[0]:line.replace("\n", "").split()[1] for line in f}

with open("stopwords.txt", "r") as f:
    stopwords = [line.replace("\n", "") for line in f][1:]

keep_words = set(frequent_words.keys()) - set(stopwords)

words_number = 20000

with open("wordlist.txt", "w") as f:
        for word in keep_words:
            if len(word) <= 2:
                continue
#                pass
            if int(frequent_words[word]) > words_number:
                f.write(word + "\n")
