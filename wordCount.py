#! /usr/bin/env python3

import os
import re
import string
import sys

# set input and output files
if len(sys.argv) is not 3:
    print('Usage: wordCount.py <input text file> <output text file>')
    exit()
input_filename = sys.argv[1]
output_filename = sys.argv[2]

# open and read input file
if not os.path.exists(input_filename):
    print('Input text file {} does not exist'.format(input_filename))
    exit()
with open(input_filename) as input_file:
    text = input_file.read()

# replace punctuation with whitespace, then split on whitespace
text = re.sub('[{}]'.format(string.punctuation), ' ', text)
words = text.lower().split()

# count words
word_counts = {}
for word in words:
    word_counts.setdefault(word, 0)
    word_counts[word] += 1

# write word counts to output file
with open(output_filename, 'w') as output_file:
    for k, v in sorted(word_counts.items()):
        output_file.write('{} {}\n'.format(k, v))
