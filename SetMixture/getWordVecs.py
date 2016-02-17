
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


size = 50
window =100
epoch = 22

dbow = Doc2Vec.load('dbow{}_{}_{}'.format(size,window,epoch))

for word in dbow.vocab:
    print word + '@' + '@'.join([str(v) for v in list(dbow[word])])