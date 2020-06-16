import enchant
import time
import pandas as pd


def combos(s):
  if not s:
    return
  yield (s,)
  for i in range(1, len(s)):
    for c in combos(s[i:]):
      yield (s[:i],) + c

def word2SW(word):
    colnames = ['word', 'count']
    # with open('unigram_freq.csv') as file:
    common_words = pd.read_csv('unigram_freq.csv', names = colnames, dtype={'word':'string','count':int})
    
    # cw = common_words.word.tolist()
    # cw_count = common_words.count.tolist()
    cw = common_words['word']
    cw_count = common_words['count']
    d = enchant.Dict("en_US")
    new_list = []
    for c in combos(word):
        count = 0
        for allWords in c:
            if not d.check(allWords) or len(allWords) == 1:
               break
            else:
                count += 1
        if count == len(c):
            new_list.append(c)
    flat_set = set()
    for subtuple in new_list:
        for item in subtuple:
            flat_set.add(item)
    d1 = pd.DataFrame(flat_set , columns = ['word'])
    df = d1.merge(common_words, on='word')
    print(df.sort_values(by = "count",ascending = False))
    # print(df)
    return new_list, flat_set

f = word2SW("camerastick")
print(f)

# def checking(word):
#     d = enchant.Dict("en_US")
#     result = d.check(word)
#     return result

# from nltk.corpus import words

# def checking2(word):
#     return word in words.words()

# f = checking("er")
# print(f)
