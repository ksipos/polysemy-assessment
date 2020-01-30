import pandas as pd
import sys
import re
import string
from pandas import Series


##### Regex
tag_pattern = re.compile("[</]+\w+>?")
number_pattern = re.compile("\d+")
#####
punctuation = string.punctuation.replace("-", "").replace("'", "") + "«»"
def remove_punc(row):
    word = str(row['word']).lower()
    if re.search(tag_pattern, word) or word.isdigit():
        word = ""
    else:
        word = re.sub(number_pattern, " ", word)
    #    word = re.sub(punctuation, '', word)
        word = word.translate(str.maketrans('', '', punctuation))
    row['word'] = word.strip()
    return row


unigrams_file = sys.argv[1]
lang=unigrams_file.split("/")[-1].split("_")[0]
stopwords = pd.read_csv(lang + "_stopwords.txt", header=None)

import csv
unigrams_list = []
with open(unigrams_file, 'r') as f:
    for line in f:
        line = line.strip()
        if len(line.split()) < 2:
            continue
        elif len(line.split()) > 2:
            line = line.split()
            count = line[0]
            word = " ".join(line[1:])
        else:
            count, word = line.split()
        row = remove_punc({'count':count, 'word':word})
        unigrams_list.append([float(row['count']), row['word']])

unigrams = pd.DataFrame(unigrams_list, columns=['count', 'word'])

import numpy as np
unigrams['word'].replace("", np.nan, inplace=True)
unigrams.dropna(subset=['word'], inplace=True)

unigrams = unigrams.groupby('word', as_index=False).sum()#.aggregate({'word': 'first', 'count': 'sum'})

unigrams = unigrams[unigrams['count']>1000] # Keep only words that appear at least 1k times
unigrams = unigrams.sort_values(by='count', ascending=False)
unigrams.to_csv(lang + "_cleared.txt", sep=' ', header=False, index=False)


wordlist = unigrams[unigrams['word'].apply(lambda word: len(word) >= 3)]
wordlist = wordlist[~wordlist['word'].isin(stopwords[0])]
wordlist['word'].drop_duplicates().head(2000).to_csv(lang + "_wordlist.txt", sep=' ', header=False, index=False)

