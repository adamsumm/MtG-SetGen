
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


size = 200
window =15
epoch = 19

dbow = Doc2Vec.load('dbowDS{}_{}_{}'.format(size,window,epoch))
dm = Doc2Vec.load('dmDS{}_{}_{}'.format(size,window,epoch))
def getConcatVec(models,token):
    return np.concatenate([model.docvecs[token] for model in models])
with open('concatCardVecs{}_{}_{}'.format(size,window,epoch),'wb') as outfile:
    for tag in dbow.docvecs.offset2doctag:
        outfile.write(tag+'@' + '@'.join([str(v) for v in getConcatVec([dbow,dm],tag)])+'\n')
    
