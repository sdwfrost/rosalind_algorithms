import sys

def scomp(k,text):
    kmers = []
    tlen = len(text)
    for i in range(tlen-k+1):
        kmers.append(text[i:i+k])
    return sorted(kmers)

def prefix(pattern):
    pre = pattern[:len(pattern)-1]
    return pre

def suffix(pattern):
    suf = pattern[1:]
    return suf

def overlapGraph(pats):
    edges = set()
    for pat1 in pats:
        p1s = suffix(pat1)
        for pat2 in pats:
            p2p = prefix(pat2)
            if p1s == p2p:
                edges.add(pat1 + ' -> ' + pat2)
    return edges
        

pats = open(sys.argv[1],'r').read().split()


edges = overlapGraph(pats)
for edge in edges:
    print edge


