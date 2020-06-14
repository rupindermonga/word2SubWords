import wordninja, os, re

# print(wordninja.split('photostick'))

# print(wordninja.split('smartphone'))

from math import log

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
with open("wordninja_words.txt") as f:
    words = f.read().split()

# words = "camerastick"

wordcost = dict((k, log((i+1)*log(len(words)))) for i,k in enumerate(words))

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
        if len(numbered)==1:
            final = min(numbered)
        else:
            final = second_smallest(numbered)
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
s ="photostick"
# s = 'smartphone'
# s="thumbgreenappleactiveassignmentweeklymetaphor"
print(infer_spaces(s))