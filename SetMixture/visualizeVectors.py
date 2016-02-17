import matplotlib.pyplot as plt
import numpy as np

cvFile = 'tfidfVec'
cardvec = []
card2vec = {}
with open(cvFile,'rb') as cardvecfile:
    for line in cardvecfile:
        line = line.rstrip().split('@')
        name = line[0]
        cardvec.append([float(v) for v in line[1:]])
        card2vec[name] = np.array(cardvec[-1])
cardvec = np.array(cardvec)

for dim in range(cardvec.shape[1]):
    hist,bins = np.histogram(cardvec[:,dim],bins=50)
    width = 0.7*(bins[1]-bins[0])
    center = (bins[:-1]+bins[1:])*0.50
    plt.bar(center,hist,align='center',width=width)
    plt.show()