import numpy as np
import re
import json
import pandas as pd
import sys
from collections import Counter
from operator import itemgetter

import csv

import time
for pca in range(4, (20 + 2), 2):
    start = time.time()
    with open("/barracuda/wsd_reduced/pca" + str(pca) + ".csv", 'r') as f:
        reader = csv.reader(f)
        labels = []
        vectors = []
        for line in reader:
            labels.append(line[0])
            vectors.append(np.array([float(i) for i in line[1].split(",")]))
    print('\n|finished loading dimensions', pca, 'in', time.time() - start, 'seconds')

    start = time.time()
    embeddings = np.array(vectors)


    minv = embeddings.min()
    embeddings = (embeddings - minv)/np.ptp(embeddings)
    number_of_embeddings, embeddings_dimension = embeddings.shape
    unique_labels = list(set(labels))
    print('|--normalized matrix in', time.time() - start, 'seconds')

    ################

    # L = 10
    L = 20
    histo_counters = []
    histoL_counter = {}
    pca_time = time.time()
    for j in range(L):
        print('|--starting layer ', j)
        start = time.time()
        # j = L
        # Number of cells along each dimension at level j
        k = 2**j
        # Determines the cells in which each vertex lies
        # along each dimension since nodes lie in the unit
        # hypercube in R^d
        T = np.floor(embeddings*k)
        T[np.where(T == k)] = k-1
        T = T.astype(int)
        for vector_index, label in enumerate(labels):
            # Identify the cell into which the i-th
            # vertex lies and increase its value by 1
            cell = ",".join([str(element) for element in T[vector_index]])
            current = histoL_counter.get(label, set())
            current.add(cell)
            histoL_counter[label] = current
            
        histo_counters.append({word: len(cells) for word, cells in histoL_counter.items()})
        print('|--finished layer', j, 'in', time.time() - start, 'seconds')
    print('|--finished all layers in', time.time() - pca_time, 'seconds')
    start = time.time()
    total_histo_counter = {}
    for current_L in range(1, L):
        for l, counters in enumerate(histo_counters[:current_L]):
            coef = 1.0/(2**(current_L-l))
            for word, v in counters.items():
                total_histo_counter[word] = total_histo_counter.get(word, 0) + (coef * (float(v)/(embeddings_dimension * 2**l)))

            tmp = [(k, round(v, 3)) for k, v in total_histo_counter.items()]
            a = sorted(tmp, key=itemgetter(1))
            with open("pyramid_output2/pca" + str(pca) + "_L" + str(current_L), 'w') as f:
                f.write("\n".join([",".join([str(j) for j in i]) for i in a]))
    print('|-- Calculated sums for pca', pca, 'in', time.time() - start, 'seconds')