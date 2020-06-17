import wordninja, os, re
from math import log
import math
import enchant
import json
import copy

# d = enchant.Dict("en_US")

# with open("wordninja_words.txt") as f:
#     original_words = f.read().split()
#     # words = f.read().split()

# words = []
# count =0
# net_count = 0
# for eachWord in original_words:
#     count +=1
#     if d.check(eachWord) and len(eachWord) != 1:
#         words.append(eachWord)
#         net_count +=1
# print(count)
# print(net_count)

with open("wordninja_words_dict.txt") as f:
    words = f.read().split()

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


# words = "camerastick"

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
        candidates = enumerate(reversed(cost[max(0, i-maxword):i]))
        # return min((c + wordcost.get(s[i-k-1:i], 9e999), k+1) for k,c in candidates)
        numbered = []
        for k, c in candidates:
            numbered.append((c + wordcost.get(s[i-k-1:i],9e999), k+1))
        # return min(numbered)
        new_numbered = copy.deepcopy(numbered)
        final = min(numbered)
        if len(numbered)==1 or math.isinf(min(numbered)[0]):
            final = final
        else:
            new_numbered.remove(final)
            if math.isinf(min(new_numbered)[0]):
                final = final
            else:    
                final = min(new_numbered)
        return final


    # Build the cost array.
    cost = [0]
    for i in range(1,len(s)+1):
        c,k = best_match(i)
        cost.append(c)

    # Backtrack to recover the minimal-cost string.
    out = []
    i = len(s)
    while i>0:
        c,k = best_match(i)
        assert c == cost[i]
        out.append(s[i-k:i])
        i -= k

    return " ".join(reversed(out))
# # s ="photostick"
# # s = 'smartphone'
# s = "aftereffect"
# # s="thumbgreenappleactiveassignmentweeklymetaphor"
# print(infer_spaces(s))