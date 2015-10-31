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

def profileNuc(pro,nuc,seq):
    for i in range(len(seq)):
        if seq[i] == nuc:
            pro[i] += 1
    return pro

def enumMers(dna,mers,d,k):
    for seq in dna:
        for i in range(len(dna)):
            if len(dna[i:i+k]) == k:
                mers.update(neighbors(dna[i:i+k],d))
def calcProb(apro,cpro,gpro,tpro,mer):
    prob = 1
    for i in range(len(mer)):
        if mer[i] == 'A':
            prob = prob * apro[i]
        if mer[i] == 'C':
            prob = prob * cpro[i]
        if mer[i] == 'G':
            prob = prob * gpro[i]
        if mer[i] == 'T':
            prob = prob * tpro[i]
    return prob


f = open(sys.argv[1],'r')
ins = f.read().split()
f.close()

sequence = ins[0]
k = int(ins[1])
apro = map(float,ins[2:2+k])
cpro = map(float,ins[2+k:2+2*k])
gpro = map(float,ins[2+2*k:2+3*k])
tpro = map(float,ins[2+3*k:2+4*k])

mers = set()

enumMers(sequence,mers,0,k)

merProbs = dict.fromkeys(mers,0)
for mer in merProbs:
    merProbs[mer] = calcProb(apro,cpro,gpro,tpro,mer)


print max(merProbs,key=lambda x: merProbs[x])

