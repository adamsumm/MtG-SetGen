import re,sys,subprocess,os,struct,math
from os import listdir
from os.path import isfile, join
from multiprocessing.dummy import Pool as ThreadPool
import json
import numpy as np
import sklearn
from sklearn import mixture

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

card2vec = {}
cardvecfile = 'dbowCardVecs50_100_22' # 'cardvectors.data'
with open(cardvecfile,'rb') as cardvectors:
    for card in cardvectors:
        card = card.rstrip().split('@')
        name = card[0]
        
        vec = [float(v) for v in card[1:-1]]
        card2vec[name] = vec

setvec = []
cards = []

import unicodedata
for card in set2cards['M14']:
    cards.append(card)
    setvec.append(card2vec[unicodedata.normalize('NFKD', card.lower()).encode('ascii','ignore')])
    
setvec = np.array(setvec)
setvec = sklearn.preprocessing.scale(setvec)
bestGMM = None
bestFit = float('inf')

from sklearn import cluster
#'diag' seems better than full
bestNC = -1
for nC in range(int(len(cards)/5),int(len(cards)/5)+1,10):
    for covar in ['tied']:
        gmm = mixture.GMM(n_components=nC, covariance_type=covar)
        gmm.fit(setvec)
        bic =  gmm.aic(setvec)
        print nC, bic
        sys.stdout.flush()
        if bic < bestFit:
            bestNC = nC
            bestFit = bic
            bestGMM = gmm
print bestNC
clusters =bestGMM.predict(setvec)
clusters2card = {ii:[] for ii in range(bestNC)}
for card,cluster in zip(cards,clusters):
    clusters2card[cluster].append(card)

for ii in range(bestNC):
    print clusters2card[ii]
'''
max_w = 50 #Max length of vocabulary entries

nameFieldPattern = re.compile("\\|(.*?)\\|.*?",re.IGNORECASE|re.DOTALL)
manaCostPattern = re.compile("(\\{.*?\\})",re.IGNORECASE|re.DOTALL)

def makevector(vocabulary,vecs,sequence):
    words = sequence.split()
    indices = []
    for word in words:
        if word not in vocabulary:
            #print("Missing word in vocabulary: " + word)
            continue
            #return [0.0]*len(vecs[0])
        indices.append(vocabulary.index(word))
    #res = map(sum,[vecs[i] for i in indices])
    res = None
    for v in [vecs[i] for i in indices]:
        if res == None:
            res = v
        else:
            res = [x + y for x, y in zip(res,v)]
    length = math.sqrt(sum([res[i] * res[i] for i in range(0,len(res))]))
    for i in range(0,len(res)):
        res[i] /= length
    return res

def sanitizeInput(cardline):
    nameMatch = nameFieldPattern.search(cardline)
    if nameMatch:
        cardline = cardline.replace(nameMatch.group(1),"") #Eliminate the name.
    cardline = cardline.replace("|"," ") #And then eliminate all the field delimiting bars.

    needsPadding = [",",".","\\",":","[","]","~","/","\"",";"]
    for symbol in needsPadding:
        cardline = cardline.replace(symbol, " " + symbol + " ")
    mcosts = re.findall(manaCostPattern,cardline)
    for match in mcosts:
        cardline = cardline.replace(match," ".join(match))
    return (nameMatch.group(1),cardline)


def getVectorData(filename):
    f = open(filename,"rb")
    words = int(f.read(4))
    size = int(f.read(4))
    vocab = [" "] * (words * max_w)
    M = []
    for b in range(0,words):
        a = 0
        while True:
            c = f.read(1)
            vocab[b * max_w + a] = c;
            if len(c) == 0 or c == ' ':
                break
            if (a < max_w) and vocab[b * max_w + a] != '\n':
                a += 1
        tmp = list(struct.unpack("f"*size,f.read(4 * size)))
        length = math.sqrt(sum([tmp[i] * tmp[i] for i in range(0,len(tmp))]))
        for i in range(0,len(tmp)):
            tmp[i] /= length
        M.append(tmp)
        
    f.close()
    return (("".join(vocab)).split(),M)


def getOriginalCardVectors(filename="corpus_encoded.txt",vectorFileName="vectors_cbow.bin"):
    cards = open(filename)
    (vocab,vecs) = getVectorData(vectorFileName)
    outvecs = []
    for cardline in cards:
        if "|" in cardline:
            (name,cleanline) = sanitizeInput(cardline)
            outvecs.append((name,makevector(vocab,vecs,cleanline)))
    cards.close()
    return (vocab,vecs,outvecs)
    
for card in getOriginalCardVectors()[2]:
    print card
'''