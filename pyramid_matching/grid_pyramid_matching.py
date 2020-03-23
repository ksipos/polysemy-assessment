import numpy as np
import re
import json
import pandas as pd
import sys
from collections import Counter
from operator import itemgetter
import csv
import time
import os

vectors_directory = "/vectors/"
output_directory = "pyramid_output/"
L = 20

if not os.path.exists(output_directory):
    os.makedirs(output_directory)

for pca in range(2, (20 + 2), 1):
    start = time.time()
    with open(vectors_directory + "/pca" + str(pca) + ".csv", 'r') as f:
        reader = csv.reader(f)
        labels, vectors = [], []
        for line in reader:
            labels.append(line[0])
            vectors.append(np.array([float(i) for i in line[1].split(",")]))
    print('\n|finished loading dimensions', pca,
          'in', time.time() - start, 'seconds')

    start = time.time()
    embeddings = np.array(vectors)

    # Normalize vectors in [0,1]
    minv = embeddings.min()
    embeddings = (embeddings - minv) / np.ptp(embeddings)
    number_of_embeddings, embeddings_dimension = embeddings.shape
    unique_labels = list(set(labels))
    print('|--normalized matrix in', time.time() - start, 'seconds')

    # List that contains the histogram counters for each level of the pyramid
    histo_counters = []
    pyramid_time = time.time()
    for j in range(L):
   		# Map that stores the cells where a word appears into (word: [cell_i, ...,
   		# cell_n])
	    histoL_counter = {}
        print('|--starting layer ', j)
        start = time.time()
        # Number of cells along each dimension at level j
        k = 2**j
        # Determines the cells in which each vertex lies
        # along each dimension since nodes lie in the unit
        # hypercube in R^d
        T = np.floor(embeddings * k)
        T[np.where(T == k)] = k - 1
        T = T.astype(int)
        for vector_index, label in enumerate(labels):
            # Identify the cell into which the i-th
            # vertex lies and increase its value by 1
            cell = ",".join([str(element) for element in T[vector_index]])
            current_word = histoL_counter.get(label, set())
            current_word.add(cell)
            histoL_counter[label] = current_word

        histo_counters.append({word: len(cells)
                               for word, cells in histoL_counter.items()})
        print('|--finished layer', j, 'in', time.time() - start, 'seconds')
    print('|--finished all layers in', time.time() - pyramid_time, 'seconds')
    start = time.time()
    total_histo_counter = {}
    # Using 'current_L' to calculate the pyramid with different L value faster
    for current_L in range(1, L):
        for l, counters in enumerate(histo_counters[:current_L]):
            coef = 1.0 / (2**(current_L - l))
            for word, cell_counter in counters.items():
                total_histo_counter[word] = total_histo_counter.get(
                    word, 0) + (coef * (float(cell_counter) / (embeddings_dimension * 2**l)))

            # Transform the dictionary for sorting and printing
            tmp = [(word, round(cell_counter, 3)) for word, cell_counter in total_histo_counter.items()]
            tmp = sorted(tmp, key=itemgetter(1))
            with open(os.join(output_directory, "pca" + str(pca) + "_L" + str(current_L)), 'w') as f:
                f.write("\n".join([",".join([str(j)
                                             for j in i]) for i in tmp]))
    print('|-- Calculated sums for pca', pca,
          'in', time.time() - start, 'seconds')
