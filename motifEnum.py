import sys

ins = open(sys.argv[1]).read().split()

k = int(ins[0])
d = int(ins[1])
seqs = ins[2:]
kmers = []

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

def mismatchCheck(pattern, check,misses):
    match = False
    misCount = 0
    for i in range(len(pattern)):
        if check[i] != pattern[i]:
            misCount += 1
    if misCount <= misses:
        match = True
    return match
            
    
def approxMatch(pattern,sequence,seqLength,misses):
    patternLength = len(pattern)
    mismatch = False
    for i in range(seqLength):
        check = sequence[i:patternLength+i]
        if len(check) == len(pattern):
            mismatch = mismatchCheck(pattern,check,misses)
        if mismatch:
            break
    return mismatch

mers = set()
goodMers = set()
for seq in seqs:
    for i in range(len(seq)):
        if len(seq[i:i+k]) == k:
            mers.update(neighbors(seq[i:i+k],d))

for mer in mers:
    good = True
    for seq in seqs:
        if not approxMatch(mer,seq,len(seq),d):
            good = False
            break
    if good:
        goodMers.add(mer)

for mer in goodMers:
    print mer,
    
