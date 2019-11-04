import sys
import string
import re

name = sys.argv[1]

print(name)
with open("llines/" + name + ".txt", "r") as f:
    indexes = [int(line.replace("\n", "")) for line in f]
print(len(indexes))
output = open("wordsentencesAugust/" + name + ".txt", 'w')
with open('sentences_full.txt', 'r') as f:
    lines = [l.replace("\n", "") for l in f]

max_length = 0
import numpy as np

for index in np.random.choice(indexes, min(len(indexes), 10000), replace=False):
    line = lines[index-1]
    l = re.sub(r'[^\x00-\x7F]+',' ', line.replace("\n", "").lower().translate(str.maketrans(' ', ' ', string.punctuation)))
    words = len(l.split())
    if words > 80:
        locations = [m.start(0) + 1 for m in re.finditer(r'[a-z]\.[A-Z]', l)]
        ls = []
        prev_loc = 0
        for loc in locations:
            ls.append(l[prev_loc:loc])
            prev_loc = loc
        ls.append(l[prev_loc:])
        for l in ls:
            words = len(l.split())
            if words > max_length:
                max_lengths = words
            output.write(l + "\n")
    else:
        output.write(l + "\n")
        if words > max_length:
            max_length = words
output.close()

