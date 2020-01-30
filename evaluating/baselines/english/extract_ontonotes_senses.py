import os
import xml.etree.ElementTree as ET


path = 'ontonotes/ontonotes-release-5.0/data/files/data/english/metadata/sense-inventories'


filenames = os.listdir(path)
senses = {}
for name in filenames:
    if '.xml' not in name:
        continue
    file_path = path + "/" + name
    print(file_path)
    word = name.split("-")[0]
    tree = ET.parse(file_path)
    tree_senses = tree.findall('sense')
    counter = senses.get(word, 0)
    for ts in tree_senses:
        if ts.attrib['name'] == 'none of the above':
            continue
        counter += 1
    senses[word] = counter

import operator

with open("ontonotes_senses.txt", "w") as f:
    for pair in sorted(senses.items(), key=operator.itemgetter(1)):
        k, v = pair
        f.write(k + "," + str(v) + "\n")

with open("pyramid_output2/pca4_L1", 'r') as f:
    words = [line.replace("\n", "").split(",")[0] for line in f]

intersection = {}
count = 0
for word in words:
    print(word)
    if word in senses:
        count += 1
    intersection[word] = senses.get(word, 0)

print(len(intersection), count)

with open("ontonotes_ranking.txt", "w") as f:
    for pair in sorted(intersection.items(), key=operator.itemgetter(1)):
        k, v = pair
        f.write(k + "," + str(v) + "\n")


