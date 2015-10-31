import sys

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

##def profileNuc(pro,nuc,seq):
##    for i in range(len(seq)):
##        if seq[i] == nuc:
##            pro[i] += 1
##    return pro

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
    #print cons, mers
    #print profile
    score = 0
    for mer in mers:
        score += hamming(cons,mer)
    #print score
    return score

f = open(sys.argv[1],'r')
ins = f.read().split()
f.close()

sequences = ins[2:]
k = int(ins[0])
t = float(ins[1])

seqlen = len(sequences[0])

bests = []
bscore = 1000

for i in range(seqlen-k+1):
    mers = []
    mers.append(sequences[0][i:i+k])
    #print mers
    profile = createProfile(mers,len(mers))
    for seq in sequences[1:]:
        mersInSeq = []
        for j in range(seqlen-k+1):
            check = seq[j:j+k]
            mersInSeq.append(check)
        mers.append(pickBest(profile,mersInSeq))
        #print mers
        profile = createProfile(mers,len(mers))
    if i == 0:
        bests = mers
        bscore = motifsScore(profile,bests)
        #print bests
    else:
        s = motifsScore(profile,mers)
        #print mers
        if s < bscore:
            bests = mers
            bscore = s
        
                    
            
#print profile
for best in bests:
    print best
    



