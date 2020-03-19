import h5py
import sys
import json
import numpy as np
import random

file_name = sys.argv[1]
word = file_name.split("/")[-1].split(".")[0]

path = "/".join(file_name.split("/")[:-1])

# Read the file containing the vectors. The key "sentence_to_index"
# contains all sentences as json
f = h5py.File(file_name, 'r')
sentences = json.loads(f.get('sentence_to_index')[0])

custom_output = open(path + "/" + word + "_vectors.txt", 'w')
for sentence, index in sentences.items():
    dataset = f.get(str(index))
    words = sentence.split()
    # Use this in order to pick only 1 word per sentence
    # Get the indexes of all instances of the word
    word_instances = [index for index,
                      indexed_word in enumerate(words) if indexed_word == word]
    # Pick an index randomly
    index = random.choice(word_instances)
    ###
    custom_output.write(
        word + " - " + ",".join([str(number) for number in dataset[index]]) + "\n")
f.close()
custom_output.close()
