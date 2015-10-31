import sys

def scomp(k,text):
    kmers = []
    tlen = len(text)
    for i in range(tlen-k+1):
        kmers.append(text[i:i+k])
    return sorted(kmers)

def prefix(pattern):
    pre = pattern[:len(pattern)]
    return pre

def suffix(pattern):
    suf = pattern[1:]
    return suf
        

pats = open(sys.argv[1],'r').read().split()

print pats[0],prefix(pats[0]),suffix(pats[0])


