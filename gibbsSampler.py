import sys
import math
import random

def hamming(pattern, check):
    match = False
    distance = 0
    for i in range(len(pattern)):
        if check[i] != pattern[i]:
            distance += 1
    return distance

def neighbors(s, d):
    l = []
    if d==0 or len(s)==0:
        return[s]
    for n in 'ACGT':
        d1 = d-1      
        if n==s[0]:
            d1 = d
        for m in neighbors(s[1:], d1):
            l.append(n + m)
    return l

def enumMers(dna,mers,d,k):
    for seq in dna:
        for i in range(len(dna)):
            if len(dna[i:i+k]) == k:
                mers.update(neighbors(dna[i:i+k],d))
def calcProb(profile,mer):
    prob = 1
    for i in range(len(mer)):
        if mer[i] == 'A':
            prob = prob * profile['A'][i]
        if mer[i] == 'C':
            prob = prob * profile['C'][i]
        if mer[i] == 'G':
            prob = prob * profile['G'][i]
        if mer[i] == 'T':
            prob = prob * profile['T'][i]
    return prob

def normalize(pro,t):
    newpro = []
    for item in pro:
        newpro.append(item/(float(t)+4))
    return newpro

def profileNuc(pro,nuc,seq):
    for i in range(len(seq)):
        if seq[i] == nuc:
            pro[i] += 1
    return pro

def createProfile(seqs, t):
    profile = createProfileDic(k)
    #print seqs
    for seq in seqs:
        for nuc,pro in profile.iteritems():
            if nuc == 'A':
                profile[nuc] = profileNuc(pro,'A',seq)
            if nuc == 'C':
                profile[nuc] = profileNuc(pro,'C',seq)
            if nuc == 'G':
                profile[nuc] = profileNuc(pro,'G',seq)
            if nuc == 'T':
                profile[nuc] = profileNuc(pro,'T',seq)
    for nuc,pro in profile.iteritems():
        if nuc == 'A':
            profile[nuc] = normalize(profile[nuc],t)
        if nuc == 'C':
            profile[nuc] = normalize(profile[nuc],t)
        if nuc == 'G':
            profile[nuc] = normalize(profile[nuc],t)
        if nuc == 'T':
            profile[nuc] = normalize(profile[nuc],t)
    return profile
    
def createProfileDic(k):
    profile = {'A':[],'C':[],'G':[],'T':[]}
    for nuc in profile.values():
        for i in range(k):
            nuc.append(1)
    return profile

def pickBest(profile,mers):
    best = (mers[0],calcProb(profile,mers[0]))
    for mer in mers[1:]:
        score = calcProb(profile,mer)
        if score > best[1]:
            best = (mer,score)
    return best[0]

def consensus(profile):
    cons= ''
    for i in range(len(profile['A'])):
        maxnuc = ('',0)
        for nuc,scores in profile.iteritems():
            if scores[i] > maxnuc[1]:
                maxnuc = (nuc,scores[i])
        cons += maxnuc[0]
    return cons

def motifsScore(profile,mers):
    cons = consensus(profile)
    score = 0
    for mer in mers:
        score += hamming(cons,mer)
    #print score
    return score

def getMers(seq,k):
    mersInSeq = []
    for i in range(len(seq)-k+1):
        mersInSeq.append(seq[i:i+k])
    return mersInSeq
            
def motifs(profile,k,sequences):
    motifs = []
    for seq in sequences:
        mersInSeq = getMers(seq,k)
        motifs.append(pickBest(profile,mersInSeq))
    return motifs

def randomizedMotifSearch(k,t,sequences):
    seqlen = len(sequences[0])

    bests = []
    mers = []
    bscore = 10000000
    
    for seq in sequences:
        rand = int(math.floor(random.random() * (len(seq)-k+1)))
        mers.append(seq[rand:k+rand])
    bests = mers
    
    while 1:
        profile = createProfile(mers,t)
        mers = motifs(profile,k,sequences)
        
        s = motifsScore(profile,mers)
        profile = createProfile(mers,t)
        #print s,bscore
        if s < bscore:
            bscore = s
            bests = mers
        else:
            return bests,bscore

def genMotifProfile(profile,seq):
    motifPro = []
    for i in range(len(seq)-k+1):
        mer = seq[i:i+k]
        score = calcProb(profile,mer)
        motifPro.append((mer,score))
    return sorted(motifPro,key=lambda x:x[1]*-1)

def pickRandomWeighted(motifProbs):
    rand = random.random()
    runTotal = float(0)
    scaledList = []
    pickedmer = motifProbs[0][0]
    for merProb in motifProbs:
        runTotal += merProb[1]
    for merProb in motifProbs:
        scaledList.append((merProb[0],merProb[1]/runTotal))
    runTotal = 0

    for scaled in scaledList:
        runTotal += scaled[1]
        if rand < scaled[1]:
            pickedmer = scaled[0]
    return pickedmer

def gibbs(k,t,N,sequences):
    mers = []
    for seq in sequences:
        rand = int(math.floor(random.random() * (len(seq)-k+1)))
        mers.append(seq[rand:k+rand])
    bests = mers
    bscore = 100000000
    i = int(math.floor(random.random() * t))
    
    for j in range(N):
        i = int(math.floor(random.random() * t))
        
        mers.pop(i)
        profile = createProfile(mers,t-1)
        motifProbs = genMotifProfile(profile,sequences[i])
        pickedMer = pickRandomWeighted(motifProbs)
        mers.insert(i,pickedMer)
        s = motifsScore(profile,mers)
        
        if s < bscore:
            bests = mers
            bscore = s
            
    return bests,bscore


######Main#########
f = open(sys.argv[1],'r')
ins = f.read().split()
f.close()

sequences = ins[3:]
k = int(ins[0])
t = float(ins[1])
N = int(ins[2])

bests = []
bscore = 100000000

for i in range(20):
    mers,s = gibbs(k,t,N,sequences)
    if s < bscore:
        bests = mers
        bscore = s

for best in bests:
    print best
print bscore
    



