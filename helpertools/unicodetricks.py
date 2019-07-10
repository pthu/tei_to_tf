
# coding: utf-8

# # Greek Unicode tricks
# 
# In this notebook, we explore how the unicodedata library works and how we can use it to convert Greek text to a number of formats. An important function is also to split punctuation from words even if it occurs in the middle of a word. 
# 
# (A lot of code in this notebook has originally been written by Dirk Roorda for which I am very thankful. Afterwards, I have done my own job with it and adjusted the original code here and there.)
# 


import pickle
from unicodedata import category, normalize
from pprint import pprint


# First we show the available categories of unicode characters available in the unicodedata library.


# Show dictionary with all unicode categories
#open_dict = open("data/unicode_cat_dict.pickle","rb")
#unicode_cat_dict = pickle.load(open_dict)
#print('These are the available categories in the unicodedata library:')
#pprint(unicode_cat_dict)

#open_dict.close()


# We now process some (poluted) Greek words and categorize the various characters present in these words. Also the difference between combined characters with accents and uncombined characters with accents will be shown.
# 

#word1 = 'Αὐτούς·Αὐτούς'
#word2 = 'Σιλωάμ?̔ὃ'
#word3 = 'Διδάσκαλε?̓'
#sen1 = 'ἄλογοι«, δι᾿ «ὧν« δῆλον ὅτι αἱ ἁμαρτίαι «μηνύονται« αἱ μὴ γεγονυῖαι κατὰ λόγον.'
#sen2 = '*polla/ me ta\ parakalou=nta/ e)sti cumbouleu=sai u(mi=n'

#for word in (word1, word2, word3):
#    print([category(x) for x in word])
#    print([x for x in normalize('NFD', word)])
#    print([category(x) for x in normalize('NFD', word)])
#    print('\n')
#print([category(x) for x in sen2])
#print([category(x) for x in 'cumbouleu=sai'])


# We now define a number of functions to process Greek text.

letter = {'L'}
letter_space = {'L', 'Z'}
dia = {'M'}
punc = {'P'}
letter_dia = {'L', 'M'}

NFD = 'NFD'
NFC = 'NFC'


def splitPuncSimple(w):
    afterWord = len(w)
    for i in range(len(w) - 1, -1, -1):
        if category(w[i])[0] not in letter:
            afterWord = i
        else:
            break
    return (w[0:afterWord], w[afterWord:]+' ')

def splitPunc(w):
    pP = 0
    for i in range(len(w)):
        if category(w[i])[0] not in letter:
            pP += 1
        else:
            break
    preWord = w[0:pP] if pP else ''
    pW = pP
    for i in range(pP, len(w)):
        if category(w[i])[0] in letter:
            pW += 1
        else:
            break
    word = w[pP:pW]
    pA = pW
    for i in range(pW, len(w)):
        if category(w[i])[0] not in letter:
            pA += 1
        else:
            break
    afterWord = w[pW:pA]
    if pA == len(w):
        afterWord += ' '
    
    rest = splitPunc(w[pA:]) if pA < len(w) else ()
    return ((preWord, word, afterWord),) + rest

def Tokenizer(sentence, udnorm='NFD'): 
    sen = normalize(udnorm, sentence)
    words = sen.split(' ')
    tokens = []
    tokenized_sentence = []
    for w in words:
        pP = 0
        for i in range(len(w)):
            if category(w[i])[0] not in letter_dia:
                pP += 1
            else:
                break
        preWord = w[0:pP] if pP else ''
        pW = pP
        for i in range(pP, len(w)):
            if category(w[i])[0] in letter_dia:
                pW += 1
            else:
                break
        word = w[pP:pW]
        pA = pW
        for i in range(pW, len(w)):
            if category(w[i])[0] not in letter_dia:
                pA += 1
            else:
                break
        afterWord = w[pW:pA]
        tokens = [word] + ([w[pA:]] if pA < len(w) else [])
        tokenized_sentence += tokens        
    return tokenized_sentence  
    

def plainMajuscule(sentence):
    return ''.join(x.upper() for x in normalize('NFD', ' '.join(sentence)) if category(x)[0] not in dia)

def plainMinuscule(sentence):
    return ''.join(x.lower() for x in normalize('NFD', ' '.join(sentence)) if category(x)[0] not in dia)

def plainCaps(w):
    return ''.join(x.upper() for x in normalize(NFD, w) if category(x)[0] in letter)

def plainLow(w):
    return ''.join(x.lower() for x in normalize(NFD, w) if category(x)[0] in letter)


# Finally, we do some texts to show how it works...

#wordBare = Tokenizer(sen1, udnorm='NFD')

#wordPlainMajuscule = plainMajuscule(wordBare)
#print(wordPlainMajuscule)

#wordPlainMinuscule = plainMinuscule(wordBare)
#print(wordPlainMinuscule)

