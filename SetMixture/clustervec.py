
import re,sys,subprocess,os,struct,math
from os import listdir
from os.path import isfile, join
from multiprocessing.dummy import Pool as ThreadPool
import gensim
from gensim.models.doc2vec import TaggedDocument
from collections import namedtuple
from gensim.models import Doc2Vec
import gensim.models.doc2vec
import pickle
from random import shuffle
import numpy as np
import sklearn
from sklearn import mixture
import json
size = 50
window = 100
epoch = 13

cardvec = []
card2vec = {}
with open('card2vec{}_{}_{}'.format(size,window,epoch),'rb') as cardvecfile:
    for line in cardvecfile:
        line = line.rstrip().split('@')
        name = line[0]
        cardvec.append([float(v) for v in line[1:]])
        card2vec[name] = np.array(cardvec[-1])
cardvec = np.array(cardvec)
#model = Doc2Vec.load('model{}_{}_{}'.format(size,window,epoch))
#cardvecs = model.docvecs

bestFit = float('inf')
bestGMM = None
bestNC = 0
bestCovar = ''
cardvec = sklearn.preprocessing.scale(cardvec)
for nC in range(20,250,10):
    for covar in ['diag','tied']:
        gmm = mixture.GMM(n_components=nC, covariance_type=covar)
        gmm.fit(cardvec)
        bic =  gmm.bic(cardvec)
        print nC,covar, bic
        sys.stdout.flush()
    if bic < bestFit:
        bestNC = nC
        bestFit = bic
        bestCovar = covar
        bestGMM = gmm
pickle.dump(bestGMM,open('cardMixtureModel.pkl','wb'))        

bestGMM = pickle.load(open('cardMixtureModel.pkl','rb'))
card2sets = {}
set2cards = {}
with open('data/allCardsMod.json') as data_file:    
    data = json.load(data_file)
    for card in data:
        card2sets[card] = []
        for mid in data[card]['multiverseids']:
            card2sets[card].append(mid['setCode'])
            if mid['setCode'] not in set2cards:
                set2cards[mid['setCode']] = []
            set2cards[mid['setCode']].append(card)

import unicodedata
cards = []
setvec = []
for card in set2cards['M10']:
    cards.append(card)
    setvec.append(card2vec[unicodedata.normalize('NFKD', card.lower()).encode('ascii','ignore').replace('-','~')])
                
 
setvec = np.array(setvec)    
clusters =bestGMM.predict(setvec)
clusters2card = {ii:[] for ii in range(70)}
for card,cluster in zip(cards,clusters):
    clusters2card[cluster].append(card)

for ii in sorted(clusters2card):
    print clusters2card[ii]            
'''
with open('card2vec{}_{}_{}'.format(size,window,epoch),'wb') as outfile:
    for index,card in  zip(range(len(cardvecs)),cardvecs):
        outfile.write(model.docvecs.index_to_doctag(index)+ '@' + '@'.join([str(v) for v in card]) + '\n')
'''
#for card in cardvecs:
#   print card