'''Example script to generate text from Nietzsche's writings.
At least 20 epochs are required before the generated text
starts sounding coherent.
It is recommended to run this script on GPU, as recurrent
networks are quite computationally intensive.
If you try this script on new data, make sure your corpus
has at least ~100k characters. ~1M is better.
'''

from __future__ import print_function
from keras.models import Sequential
from keras.layers.core import Dense, Activation, Dropout
from keras.layers.recurrent import LSTM
from keras.datasets.data_utils import get_file
import numpy as np
import random
import sys
import gc
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
window = 10
nameFieldPattern = re.compile("\\|(.*?)\\|.*?",re.IGNORECASE|re.DOTALL)
manaCostPattern = re.compile("(\\{.*?\\})",re.IGNORECASE|re.DOTALL)
cards = []
cardvec = []
card2vec = {}
cardnames= []
word2vec = {}
dim = -1
with open('dbowCardVecs50_100_22','rb') as cardvecfile:
    for line in cardvecfile:
        line = line.rstrip().split('@')
        name = line[0]
        cardvec.append([float(v) for v in line[1:]])
        card2vec[name] = np.array(cardvec[-1])
cardvec = np.array(cardvec)

minWordVec = float('inf')
with open('dbowWordVecs_50_100_22','rb') as wvFile:
    for line in wvFile:
        card = line.rstrip().split('@')
        name = card[0]
        name = name.replace('!','@')
        word2vec[name] = np.array([float(v) for v in card[1:]])
        minWordVec = min(minWordVec,np.linalg.norm(word2vec[name]))
        dim = len(word2vec[name])
print(minWordVec)

def vecs2words(vecs,dist = lambda x,y: np.linalg.norm(x-y)):
    output = []
    for v in vecs:
        minDist = float('inf')
        bestWord = ''
        for word,wv in word2vec.items():
            d = dist(v,x)
            if d < minDist:
                minDist = d
                bestWord = word
        output.append(bestWord)
    return output

with open("corpus_encoded.txt",'rb') as corpus:
    for card in corpus:
        nameMatch = nameFieldPattern.search(card)
        if nameMatch:
            cardnames.append(nameMatch.group(1))
cardLength = -1            
cards =[]
with open("convertedcorpus.txt",'rb') as corpus:
    for name,card in zip(cardnames,corpus):
        #print name,card.split(' ')
        card = card.split(' ')
        cardT = []
        
        for ii in range(window-1):
            cards.append(card2vec[name]*0)
        cards.append(card2vec[name])
        for w in card:
            if w != ''  and '\n' not in w:
                cards.append(word2vec[w])
                
cards = cards[:int(len(cards)/8)]
print((len(cards)-window,window,dim))
gc.collect()
print((len(cards)-window)*window*dim*32.0/1000.0/1000.0)
X = np.zeros((len(cards)-window,window,dim))
y  = np.zeros((len(cards)-window,dim))
for ii,card in enumerate(cards):
    if ii + window >= len(y):
        break
    for t in range(window):        
        X[ii,t,:] = cards[ii+t]
    y[ii] = cards[ii+window]

# build the model: 2 stacked LSTM
print('Build model...')
model = Sequential()
model.add(LSTM(128, return_sequences=True, input_shape=(window, dim)))
model.add(Dropout(0.2))
model.add(LSTM(128, return_sequences=False))
model.add(Dropout(0.2))
model.add(Dense(dim))
tol = 0.01
model.compile(loss='mse', optimizer='rmsprop')
json_string = model.to_json()
for iteration in range(1, 60):
    print()
    print('-' * 50)
    print('Iteration', iteration)
    model.fit(X, y, batch_size=10, nb_epoch=1)
    model.save_weights('vecLSTM{}.h5'.format(iteration))
    for name in ['lightning bolt','runeclaw bear','counterspell']:
        words = [card2vec[name]]
        pred = np.ones(dim)
        maxLen = 150
        while np.linalg.norm(pred) > tol:
            if maxLen <= 0:
                break
            maxLen -= 1
            x = np.zeros((1,window,dim))
            for ii in range(len(words)-1,max(len(words)-window,-1),-1):
                x[0,window-len(words)+ii,:] = words[ii]
            pred = model.predict(x)
            words.append(pred)
        print(' '.join(vecs2words(words[1])))
                