
# coding: utf-8
import operator
from functools import reduce
from unicodedata import category, normalize, decomposition, lookup

# Definition of unicodedata categories
letter = {'L'}
dia = {'M'}
punc = {'P'}
letter_dia = {'L', 'M'}

# unicodedata normalize norm
udnorm = 'NFD'

def splitWord(word, norm=udnorm): 
    w = normalize(udnorm, word)
    tokens = ()
    pP = 0
    for i in range(len(w)):
        if category(w[i])[0] not in letter:
            pP += 1
        else:
            break
    pW = pP
    for i in range(pP, len(w)):
        if category(w[i])[0] in letter_dia:
            pW += 1
        else:
            break
    realWord = w[pP:pW]
    pA = pW
    for i in range(pW, len(w)):
        if category(w[i])[0] not in letter:
            pA += 1
        else:
            break
    return (realWord,) + (splitWord(w[pA:]) if pA < len(w) else ())


def tokenize(sentence, norm=udnorm):
    return reduce(
        operator.add,
        (splitWord(word, norm=udnorm) for word in sentence.strip().split()),
        (),
    )


def strip_accents(word):
    return ''.join(c for c in normalize('NFD', word.lower())
                  if category(c)[0] in letter)

