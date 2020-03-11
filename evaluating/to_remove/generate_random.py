import os
import random
import numpy as np

baselines = [name for name in os.listdir(".") if '.txt' in name and 'random' not in name]

with open('frequency_ranking.txt', 'r') as f:
    words = [line.replace("\n", "").split(",")[0] for line in f]

# rankings = [0] * len(words)
# for baseline in baselines:
#     with open(baseline, 'r') as f:
#         rank = [float(line.replace("\n", "").split(",")[1]) for line in f]
#         random.shuffle(rank)
#         for i, v in enumerate(rank):
#             rankings[i] += v
rankings = list(np.random.choice(range(0,len(words)), len(words), replace=False))
random.shuffle(rankings)
random.shuffle(words)
output = open('random_ranking.txt', 'w')
for index, word in enumerate(words):
    # output.write(word + "," + str(rankings[index]/float(len(baselines))) + "\n")
    output.write(word + "," + str(rankings[index]) + "\n")
output.close()

# output = open('random2_ranking.txt', 'w') 
# random.shuffle(words)
# for index, word in enumerate(words):
#         output.write(word + "," + str(index) + "\n")
# output.close()

