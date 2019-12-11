import h5py
import sys
import json
import numpy as np
import random

file_name = sys.argv[1]
word = file_name.split("/")[-1].split(".")[0]
path = "/".join(file_name.split("/")[:-1])

f = h5py.File(file_name, 'r')
#output = h5py.File(path + "/" + word + "_reduced.hdf5", 'w')
custom_output = open(path + "/" + word + "_vectors.txt", 'w')
sentences = json.loads(f.get('sentence_to_index')[0])
word_counter = 0
for sentence, index in sentences.items():
    dataset = f.get(str(index))
    words = sentence.split()
    ### Use this in order to pick only 1 word per sentence
    word_instances = [index for index, index_word in enumerate(words) if index_word == word]
    index = random.choice(word_instances)
    ###
    #output.create_dataset(str(word_counter), data=dataset[index])
    custom_output.write(word + " - " + ",".join([str(number) for number in dataset[index]]) + "\n")
    word_counter += 1
f.close()
#output.close()
custom_output.close()
