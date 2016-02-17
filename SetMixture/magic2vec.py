
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

def sanitizeInput(cardline):
    nameMatch = nameFieldPattern.search(cardline)
    if nameMatch:
        cardline = cardline.replace(nameMatch.group(1),"") #Eliminate the name.
    cardline = cardline.replace("|"," | ") #And then eliminate all the field delimiting bars.
    counter = 0
    while cardline.find("|") > -1:
        cardline = cardline[:cardline.find("|")]  + str(counter) + cardline[cardline.find("|")+1:]
        counter += 1

    needsPadding = [",",".","\\",":","[","]","~","/","\"",";"]
    for symbol in needsPadding:
        cardline = cardline.replace(symbol, " " + symbol + " ")
    mcosts = re.findall(manaCostPattern,cardline)
    for match in mcosts:
        cardline = cardline.replace(match," ".join(match))
    return (nameMatch.group(1),cardline)

def convertEncodedCorpusForTraining(filename="corpus_encoded.txt",outname="convertedcorpus.txt"):
    f = open(filename)
    outputFile = open(outname,'w')
    for cardline in f:
        if "|" in cardline: #Skip if it's an empty line
            outputFile.write(sanitizeInput(cardline)[1] + "\n")
    f.close()
    outputFile.close()    
def getConcatVec(models,token):
    return np.concatenate([model.docvecs[token] for model in models])
def concatMostSimilar(pos,models):
    basevec = getConcatVec(models,pos)
    dist2card = {}
    for tag in models[0].docvecs.offset2doctag:
        othervec = getConcatVec(models,tag)
        dist = np.dot(basevec/np.linalg.norm(basevec),othervec/np.linalg.norm(othervec))
        dist2card[dist] = tag
    return [dist2card[dist] for dist in sorted(dist2card)[-5:]]
Card = namedtuple('Card', 'words tags')
cards = []

cardnames= []

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
        for w in card:
            if w != ''  and w != '\r\n':
                cardT.append(w)
        cards.append(Card(cardT,[name]))
       
train = True

size = 50
window =150
if train:       
    epochs = 100
    print 'building model'
    from gensim.test.test_doc2vec import ConcatenatedDoc2Vec
    dbow = Doc2Vec(dm=0,dbow_words=1,dm_mean=0, dm_concat=1, size=size, window=window, negative=1, hs=1, min_count=0, workers=3)
    #dm = Doc2Vec(dm=1,dm_mean=1, dm_concat=0, size=size, window=window, negative=5, hs=0, min_count=1, workers=3,sample=.1)
    #concat = ConcatenatedDoc2Vec([dbow,dm])
    print 'building vocab'
    
    dbow.build_vocab(cards)
   # dm.build_vocab(cards)
    for epoch in range(epochs):
        print epoch
        sys.stdout.flush()
        shuffle(cards)
        dbow.train(cards)
        #dm.train(cards)
        
        print 'dbow',dbow.docvecs.most_similar('lightning bolt', topn=5)
        print 'dbow',dbow.docvecs.most_similar('runeclaw bear', topn=5)
        print 'dbow',dbow.docvecs.most_similar('counterspell', topn=5)
        dbow.save('dbowNonRand{}_{}_{}'.format(size,window,epoch))
        
        #print 'dm',dm.docvecs.most_similar('lightning bolt', topn=5)
        #print 'dm',dm.docvecs.most_similar('runeclaw bear', topn=5)
        #print 'dm',dm.docvecs.most_similar('counterspell', topn=5)
        #dm.save('dmDS{}_{}_{}'.format(size,window,epoch))
        
        #p#rint 'concat',concatMostSimilar('lightning bolt',[dbow,dm])
        #print 'concat',concatMostSimilar('runeclaw bear', [dbow,dm])
        #print 'concat',concatMostSimilar('counterspell', [dbow,dm])
        