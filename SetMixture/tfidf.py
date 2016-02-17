from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import matplotlib.pyplot as plt
from scipy import linalg
import sys
from sklearn.decomposition import PCA, FactorAnalysis
from sklearn.covariance import ShrunkCovariance, LedoitWolf
from sklearn.cross_validation import cross_val_score
from sklearn.grid_search import GridSearchCV
import re
cards = []
cardnames = []
nameFieldPattern = re.compile("\\|(.*?)\\|.*?",re.IGNORECASE|re.DOTALL)
manaCostPattern = re.compile("(\\{.*?\\})",re.IGNORECASE|re.DOTALL)
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
        cards.append(' '.join(cardT))
        
vectorizer = TfidfVectorizer(min_df = 5,max_df = 0.5,ngram_range = (1,2))
X = vectorizer.fit_transform(cards).toarray()

n_components = np.arange(50,80, 5)  # options for n_components
print X.shape

fa = PCA()

fa_scores = []
for n in n_components:
    print n
    
    sys.stdout.flush()
    fa.n_components = n
    fa.fit(X)
    fa_scores.append(fa.score(X))
    print '\t',fa_scores[-1]
    

fa.n_components = n_components[np.argmax(fa_scores)]
Y = fa.fit_transform(X)

for name,ii in zip(cardnames,range(len(Y))):
    print name+'@'+ '@'.join(str(v) for v in list(Y[ii,:]))