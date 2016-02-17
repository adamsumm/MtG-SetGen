import numpy as np

cvFile = 'dbowWVCardVecs_50_100_22'
cardvec = []
card2vec = {}
with open(cvFile,'rb') as cardvecfile:
    for line in cardvecfile:
        line = line.rstrip().split('@')
        name = line[0]
        cardvec.append([float(v) for v in line[1:]])
        card2vec[name] = np.array(cardvec[-1])
cardvec = np.array(cardvec)

def findClosest(name):
    vec = card2vec[name]
    vec /= np.linalg.norm(vec)
    dists = {}
    for other in card2vec:
        if other != name:
            otherVec = card2vec[other]
            otherVec /= np.linalg.norm(otherVec)
            dist = np.dot(vec,otherVec)
            if dist not in dists:
                dists[dist]  = []
            dists[dist].append(other)
    return [(dist,dists[dist]) for dist in sorted(dists.keys())[-5:]]

def findClosestL2(name):
    vec = card2vec[name]
    dists = {}
    for other in card2vec:
        if other != name:
            otherVec = card2vec[other]
            dist = np.linalg.norm(vec-otherVec)
            if dist not in dists:
                dists[dist]  = []
            dists[dist].append(other)
    return [(dist,dists[dist]) for dist in sorted(dists.keys())[:5]]

    
print findClosest('lightning bolt')
print findClosest('runeclaw bear')
print findClosest('counterspell')
print '\n'

print findClosestL2('lightning bolt')
print findClosestL2('runeclaw bear')
print findClosestL2('counterspell')