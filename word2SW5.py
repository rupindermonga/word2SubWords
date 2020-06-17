import wordninja, os, re
from math import log
import math, copy
import enchant, time
import json
from heapq import nsmallest
import pandas as pd

# d = enchant.Dict("en_US")


'''
#old file writing into new
with open("wordninja_words.txt") as f:
    original_words = f.read().split()
    # words = f.read().split()

words = []
with open("wordninja_words_dict.txt", 'w') as f:
    for eachWord in original_words:
        if d.check(eachWord) and len(eachWord) != 1:
            words.append(eachWord)
            f.write('%s\n' % eachWord)
'''
with open("wordninja_words_dict.txt") as f:
    words = f.read().split()


# Build a cost dictionary, assuming Zipf's law and cost = -math.log(probability).
# words = open("words-by-frequency.txt").read().split()

wordcost = dict((k, log((i+1)*log(len(words)))) for i,k in enumerate(words))

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
        candidates2 = enumerate(reversed(cost2[max(0, i-maxword):i]))

        final0 = min((c0 + wordcost.get(s[i-k0-1:i], 9e999), k0+1) for k0,c0 in candidates0)

        numbered1 = []
        for k1, c1 in candidates1:
            numbered1.append((c1 + wordcost.get(s[i-k1-1:i],9e999), k1+1))
        # return min(numbered)
        new_numbered1 = copy.deepcopy(numbered1)
        if len(numbered1)==1 or math.isinf(min(numbered1)[0]):
            final1 = min(numbered1)                                                     
        else:
            new_numbered1.remove(min(numbered1))
            if math.isinf(min(new_numbered1)[0]):
                final1 = min(numbered1)
            else:
                final1 = min(new_numbered1)
        
        numbered2 = []
        for k2, c2 in candidates2:
            numbered2.append((c2 + wordcost.get(s[i-k2-1:i],9e999), k2+1))

        new_numbered2 = copy.deepcopy(numbered2)
        if len(numbered2) == 1 or math.isinf(min(numbered2)[0]):
            final2 = min(numbered2)
        elif len(numbered2) == 2:
            new_numbered2.remove(min(numbered2))
            if math.isinf(min(new_numbered2)[0]):
                final2 = min(numbered2)
            else:
                final2 = min(new_numbered2)
        else:
            new_numbered2.remove(min(numbered2))
            if math.isinf(min(new_numbered2)[0]):
                final2 = min(numbered2)
            else:
                new_numbered2.remove(min(new_numbered2))
                final2 = min(new_numbered2)

        return final0, final1, final2

    # Build the cost array.
    
    cost0 = [0]
    cost1 = [0]
    cost2 = [0]
    for i in range(1,len(s)+1):
        c0,k0 = best_match(i)[0]
        c1,k1 = best_match(i)[1]
        c2, k2 = best_match(i)[2]
        cost0.append(c0)
        cost1.append(c1)
        cost2.append(c2)

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

    out2 = []
    i = len(s)
    while i>0:
        c2,k2 = best_match(i)[2]
        assert c2 == cost2[i]
        out2.append(s[i-k2:i])
        i -= k2

    return s, " ".join(reversed(out0)), " ".join(reversed(out1)), " ".join(reversed(out2))


# f = 'aftereff'

start_time = time.time()
with open("compound_words.txt") as f:
    compoundWords = f.read().split()

final_result = []
for eachWord in compoundWords:
    final_result.append(infer_spaces(eachWord))
df = pd.DataFrame(final_result, columns = ["compound_word", "split_1", "split_2", "split_3"])

df.to_csv('final_result2.csv')

print(time.time()-start_time)

