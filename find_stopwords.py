'''
Identify stopwords in a text file
'''

from collections import Counter

counts = Counter()

with open('eng/all_text.txt') as f:
    text = f.readlines()
    for line in text:
        words = set(line.split())
        counts.update(words)

print(counts.most_common(100))
