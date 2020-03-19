import sys
import string
import re
import os
import numpy as np
from nltk.tokenize import sent_tokenize

corpus = sys.argv[1]
lines_files_dir = sys.argv[2]
output_directory = sys.argv[3]
threshold = int(sys.argv[4])

# Load the corpus in memory
with open(corpus, 'r') as f:
    corpus_lines = [l.replace("\n", "") for l in f]

line_files = sorted(os.listdir(lines_files_dir))
exclude_finished = [n.split(".")[0] for n in os.listdir(output_directory)]
for name in file_names:
    if name in exclude_finished:
        continue
    print(name)
    # Read the corresponding file that contains the indexes of the lines where
    # the word appears into
    with open(lines_files_dir + "/" + name, "r") as f:
        indexes = [int(line.replace("\n", "")) for line in f]

    stored_sentences = []
    for index in indexes:
        line = corpus_lines[index - 1]
        # Use a regular expression to split the line into sentences
        sentences = re.split(r'(?<=[^A-Z].[.?]) +(?=[A-Z])', line)
        tmp_sentences = []
        for s in sentences:
            tmp_sentences += s.split("\n")
        sentences = tmp_sentences
        # Find the sentence that the word appears into and discard the sentences with more than 80 characters
        for s in sentences:
            s = re.sub(r'[^\x00-\x7F]+', ' ', s.replace("\n",
                                                        "").lower().translate(str.maketrans(' ', ' ', string.punctuation)))
            if len(s.split()) > 80:
                continue
            if name in s.split(): # Split the sentence to check the word is one of the tokens
                stored_sentences.append(s)
    if len(stored_sentences) < threshold:
        continue
    output = open(output_directory + "/" + name + ".txt", 'w')
    # Shuffle the sentences and store them
    for sentence in np.random.choice(stored_sentences, min(len(stored_sentences), threshold), replace=False):
        output.write(sentence + "\n")
    output.close()
~
