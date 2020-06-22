import wordninja, os, re
from math import log
import math
import json
from heapq import nsmallest
import pandas as pd

with open("wordninja_words.txt") as f:
    words = f.read().split()

def smallest(numbers):
    min_list = []
    for eachTuple in numbers:
        min_list.append(eachTuple[0])
    small_numbers = nsmallest(3, min_list)
    try:
        second_min = small_numbers[1]
    except:
        second_min = small_numbers[0]
    
    try:
        third_min = small_numbers[2]
    except:
        try:
            third_min = small_numbers[1]
        except:
            third_min = small_numbers[0]

    position1 = min_list.index(second_min)
    position2 = min_list.index(third_min)
    return numbers[position1], numbers[position2] 


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
    s = s.lower()
    
    def best_match(i):
        
        candidates0 = enumerate(reversed(cost0[max(0, i-maxword):i]))
        candidates1 = enumerate(reversed(cost1[max(0, i-maxword):i]))
        candidates2 = enumerate(reversed(cost2[max(0, i-maxword):i]))

        numbered0 = []
        for k0, c0 in candidates0:
            numbered0.append((c0 + wordcost.get(s[i-k0-1:i],9e999), k0+1))
        
        final0 = min(numbered0)



        # final0 = min((c0 + wordcost.get(s[i-k0-1:i], 9e999), k0+1) for k0,c0 in candidates0)

        numbered1 = []
        for k1, c1 in candidates1:
            numbered1.append((c1 + wordcost.get(s[i-k1-1:i],9e999), k1+1))
        count1 = sum(1 if x[0] < 9e999 else 0 for x in numbered1)
        
        if count1 == 1:
            final1 = min(numbered1)
        else:
            final1 = smallest(numbered1)[0]
        
        numbered2 = []
        for k2, c2 in candidates2:
            numbered2.append((c2 + wordcost.get(s[i-k2-1:i],9e999), k2+1))
        
        count2 = sum(1 if x[0] < 9e999 else 0 for x in numbered2)

        if count2 > 2:
            final2 = smallest(numbered2)[1]
        elif count2 == 2:
            final2 = smallest(numbered2)[0]
        else:
            final2 = min(numbered2)
            
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

    return [s, " ".join(reversed(out0)), " ".join(reversed(out1)), " ".join(reversed(out2))]
# s ="Fire HD 10 Tablet with Alexa Hands-Free, 10.1 inch 1080p Full HD Display, 32 GB, Marine Blue (Previous Generation - 7th)"
s = "Display"
# s = "Fire HD 10 Tablet with Alexa Hands-Free, 10.1 inch 1080p Full HD Display, 32 GB, Marine Blue (Previous Generation - 7th)"
print(infer_spaces(s))


# print(s2)
# print(wordninja.split(s2))