import wordninja, os, re
from math import log
import math, time
import json
import copy
import pandas as pd

with open("wordninja_words_dict.txt") as f:
    words = f.read().split()

# with open("wordninja_words_dict2.txt") as f:
#     words = f.read().split()


def second_smallest(numbers):
    m1, m2 = (float('inf'), 1), (float('inf'), 1)
    for x in numbers:
        if x[0] <= m1[0]:
            m1, m2 = x, m1
        elif x[0] < m2[0]:
            m2 = x
    return m2
# Build a cost dictionary, assuming Zipf's law and cost = -math.log(probability).
# words = open("words-by-frequency.txt").read().split()


wordcost = dict((k, log((i+1)*log(len(words)))) for i,k in enumerate(words))

# with open('result.json', 'w') as fp:
#     json.dump(wordcost, fp)

maxword = max(len(x) for x in words)

def infer_spaces(s):
    """Uses dynamic programming to infer the location of spaces in a string
    without spaces."""
    
    # Find the best match for the i first characters, assuming cost has
    # been built for the i-1 first characters.
    # Returns a pair (match_cost, match_length).
    def best_match(i):
        candidates0 = enumerate(reversed(cost0[max(0, i-maxword):i]))
        candidates1 = enumerate(reversed(cost1[max(0, i-maxword):i]))
        final0 =  min((c0 + wordcost.get(s[i-k0-1:i], 9e999), k0+1) for k0,c0 in candidates0)
        numbered1 = []
        for k1, c1 in candidates1:
            numbered1.append((c1 + wordcost.get(s[i-k1-1:i],9e999), k1+1))

        if len(numbered1)==1 or math.isinf(second_smallest(numbered1)[0]):
            final1 = min(numbered1)
        else:
            final1 = second_smallest(numbered1)
        return final0, final1


    # Build the cost array.
    cost0 = [0]
    cost1 = [0]
    for i in range(1,len(s)+1):
        c0,k0 = best_match(i)[0]
        c1,k1 = best_match(i)[1]
        cost0.append(c0)
        cost1.append(c1)

    # Backtrack to recover the minimal-cost string.
    out0 = []
    i = len(s)
    while i>0:
        c0,k0 = best_match(i)[0]
        assert c0 == cost0[i]
        out0.append(s[i-k0:i])
        i -= k0

    out1 = []
    i = len(s)
    while i>0:
        c1,k1 = best_match(i)[1]
        assert c1 == cost1[i]
        out1.append(s[i-k1:i])
        i -= k1



    return s, " ".join(reversed(out0)), " ".join(reversed(out1))

f = "photostick"
print(infer_spaces(f))

start_time = time.time()
with open("compound_words.txt") as f:
    compoundWords = f.read().split()

final_result = []
for eachWord in compoundWords:
    final_result.append(infer_spaces(eachWord))
df = pd.DataFrame(final_result, columns = ["compound_word", "split_1", "split_2"])

df.to_csv('final_result3.csv')

print(time.time()-start_time)
