import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import re
import json
import pandas as pd
import h5py
import operator
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
import scipy.cluster.hierarchy as hcluster
import pickle
import sys

import csv

import time
for pca in range(4, (20 + 2), 2):
    start = time.time()
    with open("/barracuda/wsd_reduced/pca"+str(pca)+".csv", 'r') as f:
        reader = csv.reader(f)
        labels = []
        vectors = []
        for line in reader:
            # if line[0] not in ['cat', 'animal', 'house', 'programming', 'python']:
            #     continue
            # if line[0] not in ['python']: 
                # continue
            labels.append(line[0])
            vectors.append(np.array([float(i) for i in line[1].split(",")]))
    print('|finished loading dimensions', pca, 'in', time.time() - start, 'seconds')

    start = time.time()
    embeddings = np.array(vectors)


    minv = embeddings.min()
    orig = embeddings
    embeddings = (embeddings - minv)/np.ptp(embeddings)
    unique_labels = list(set(labels))
    print('|-normalized matrix in', time.time() - start, 'seconds')

    ################
    import numpy as np

    # L = 10
    d = embeddings.shape[0]
    for L in range(1,15):
        histo_counters = []
        histoL_counter = dict.fromkeys(set(labels), set())
        number_of_embeddings, embeddings_dimension = embeddings.shape
        for j in range(L):       
            # j = L
            # Number of cells along each dimension at level j
            k = 2**j
            # Determines the cells in which each vertex lies
            # along each dimension since nodes lie in the unit
            # hypercube in R^d
            D = np.zeros((d, k))
            T = np.floor(embeddings*k)
            T[np.where(T == k)] = k-1
            for vector_index in range(number_of_embeddings):
                label = labels[vector_index]
                cell = ''
                for q in range(embeddings_dimension):
                    # Identify the cell into which the i-th
                    # vertex lies and increase its value by 1
                    D[q, int(T[vector_index, q])] += 1
                    cell += str(int(T[vector_index, q])) + ","
                histoL_counter[label].add(cell[:-1])
            new_current = {}
            for k, v in histoL_counter.items():
                new_current[k] = len(v)
            histo_counters.append(new_current)

        # print(histo_counters)
        from collections import Counter
        freq_weight = Counter(labels)
        total_histo_counter = {}
        for l, counters in enumerate(histo_counters):
            coef = 1.0/(2**(L-l))
            for k, v in counters.items():
                total_histo_counter[k] = total_histo_counter.get(k, 0) + (coef * (float(v)/d * 2**l ))
        for k, v in total_histo_counter.items():
            total_histo_counter[k] = v/float(freq_weight[k])
        # import operator

        # # print(max(total_histo_counter.items(), key=operator.getter(1))[:5])
        tmp = [(k, v) for k, v in total_histo_counter.items()]
        from operator import itemgetter
        a = sorted(tmp, key=itemgetter(1))
        with open("pyramid_output2/pca" + str(pca) + "_L" + str(L), 'w') as f:
            f.write("\n".join([",".join([str(j) for j in i]) for i in a]))
        # with open("pyramid_output2/unsorted_pca" + str(pca) + "_L" + str(L), 'w') as f:
        #     f.write("\n".join([k + "," + str(v) for k, v in total_histo_counter.items()]))
