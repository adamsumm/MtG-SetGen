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
cardLength = -1            
cards =[]
with open("convertedcorpus.txt",'rb') as corpus:
    for name,card in zip(cardnames,corpus):
        #print name,card.split(' ')
        card = card.split(' ')
        cardT = []
        
        
        cardVec = []
        for w in card:
            if w != ''  and w != '\r\n':
                cardVec.append(word2vec[w])
        cardVec = np.array(cardVec)
        cardLength = max(len(cardVec),cardLength)
        cards.append(cardVec)
        
X = np.zeros((len(cards),cardLength+1,dim))
y  = np.zeros((len(cards),dim))
for ii,card in enumerate(cards):
    X[ii,1:card.shape[0]+1,:] = card
    X[ii,0,:] = cardvec[ii]
    y[ii] = cardvec[ii]

# build the model: 2 stacked LSTM
print('Build model...')
model = Sequential()
model.add(LSTM(256, return_sequences=True, input_shape=(cardLength, dim)))
model.add(Dropout(0.2))
model.add(LSTM(256, return_sequences=False))
model.add(Dropout(0.2))
model.add(Dense(dim))

model.compile(loss='cosine_proximity', optimizer='rmsprop')
json_string = model.to_json()
for iteration in range(1, 60):
    print()
    print('-' * 50)
    print('Iteration', iteration)
    model.fit(X, y, batch_size=1, nb_epoch=1)
    model.save_weights('vecLSTM.h5')