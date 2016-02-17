import re,sys,subprocess,os,struct,math
from os import listdir
from os.path import isfile, join
from multiprocessing.dummy import Pool as ThreadPool
import gensim
from gensim.models.doc2vec import TaggedDocument
from collections import namedtuple
from gensim.models import Doc2Vec
import gensim.models.doc2vec
import numpy as np
from random import shuffle

nameFieldPattern = re.compile("\\|(.*?)\\|.*?",re.IGNORECASE|re.DOTALL)
manaCostPattern = re.compile("(\\{.*?\\})",re.IGNORECASE|re.DOTALL)
cards = []

cardnames= []
word2vec = {}
dim = -1
with open('dbowWordVecs_50_100_22','rb') as wvFile:
    for line in wvFile:
        card = line.rstrip().split('@')
        name = card[0]
        name = name.replace('!','@')
        word2vec[name] = np.array([float(v) for v in card[1:]])
        dim = len(word2vec[name])


with open("corpus_encoded.txt",'rb') as corpus:
    for card in corpus:
        nameMatch = nameFieldPattern.search(card)
        if nameMatch:
            cardnames.append(nameMatch.group(1))
            
with open("convertedcorpus.txt",'rb') as corpus:
    for name,card in zip(cardnames,corpus):
        #print name,card.split(' ')
        card = card.split(' ')
        cardT = []
        cardVec = np.zeros(dim)
        for w in card:
            if w != ''  and w != '\r\n':
                cardVec += word2vec[w]
        print name + '@' + '@'.join([str(v) for v in list(cardVec)])