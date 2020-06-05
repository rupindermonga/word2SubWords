import enchant


def combos(s):
  if not s:
    return
  yield (s,)
  for i in range(1, len(s)):
    for c in combos(s[i:]):
      yield (s[:i],) + c

def word2SW(word):
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
    return new_list

f = word2SW("nonstick")
print(f)
