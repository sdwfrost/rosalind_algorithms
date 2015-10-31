import sys
import math
import random
from copy import deepcopy

def scomp(k,text,sort):
    kmers = []
    tlen = len(text)
    for i in range(tlen-k+1):
        kmers.append(text[i:i+k])
    if sort:
        return sorted(kmers)
    else:
        return kmers

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


#So much cleaner
def deBrujnFast(edges):
    merSet = set()
    
    for e in edges:
        merSet.add(prefix(e))
        merSet.add(suffix(e))
    nodes = dict.fromkeys(merSet,'')
    
    for e in edges:
        #print e
        if nodes[prefix(e)] == '':
            nodes[prefix(e)] = [suffix(e)]
        else:
            nodes[prefix(e)].append(suffix(e))
    return nodes

def deBrujnPaired(edges):
    nodeSet = set()
    

    for e in edges:
        mers = e.split('|')
        pre1 = prefix(mers[0])
        pre2 = prefix(mers[1])
        suf1 = suffix(mers[0])
        suf2 = suffix(mers[1])
        nodeSet.add(pre1+'|'+pre2)
        nodeSet.add(suf1+'|'+suf2)

    nodes = dict.fromkeys(nodeSet,[])
    for e in edges:
        mers = e.split('|')
        pre1 = prefix(mers[0])
        pre2 = prefix(mers[1])
        suf1 = suffix(mers[0])
        suf2 = suffix(mers[1])
        if nodes[pre1+'|'+pre2] == []:
            nodes[pre1+'|'+pre2] = [suf1+'|'+suf2]
        else:
            nodes[pre1+'|'+pre2].append(suf1+'|'+suf2)
    return nodes
        
        

    
    
#Don't use this, see above
def deBrujn(edges):
    nodes = []

    #create the initial nodes
    for i in range(len(edges)):
        if i != len(edges)-1:
            nodes.append((prefix(edges[i]),edges[i]))
        else:
            nodes.append((prefix(edges[i]),edges[i]))
            nodes.append((suffix(edges[i]),''))

    dbNodes = []
    nadded = []

    #join repeated nodes edges
    for node1 in nodes:
        nodet = ('','')
        found = False
        for node2 in nodes:
            if node1[0] == node2[0] and node1 != node2:
                nodet = (node1[0],','.join([nodet[1],node1[1],node2[1]]))
                found = True

        #only add node if not identical node already processed (deletion)
        if found and not nodet[0] in nadded:
            dbNodes.append(nodet)
            nadded.append(nodet[0])
        elif not node1[0] in nadded:
            dbNodes.append(node1)
            nadded.append(node1[0])

    nodes = sorted(dbNodes)
    dbNodes = []

    #create adjacency list using node and edges.
    for node in nodes:
        edges = node[1].split(',')
        second = []
        for edge in edges:
            if edge != '':
                second.append(suffix(edge))
        #second = ','.join(second)
        if second != '':
            dbNodes.append((node[0],second))

    nodes = {}
    for dbn in dbNodes:
        nodes[dbn[0]] = dbn[1]
    return nodes



###############  Eulerian Cycle  #############################

def ecy(nodes,start):
    more = True
    cyc = []
    pos = start
    while more:
        cyc.append(pos)
        try:
            try:
                n = nodes[pos].pop()
            except IndexError:
                more = False
            if len(nodes[pos]) == 0:
                del nodes[pos]
            pos = n
        except KeyError:
            more = False
    return cyc,nodes
        
        
    
def eulerianCycle(nodes):
    f = True
    i = 0
    more = True
    while more:
        if f:
            cyc,nodes = ecy(nodes,nodes.keys()[0])
            f = False
            #print '->'.join(cyc)
        else:
            start = cyc[i]
            try:
                subcyc,nodes = ecy(nodes,start)
            except KeyError:
                i += 1
                continue
            if len(subcyc) > 1:
                #print 'before:','->'.join(cyc)
                #print 'sub:','->'.join(subcyc)
                cyc = cyc[:i] + subcyc + cyc[i+1:]
                #print 'after:','->'.join(cyc)
        if len(nodes) == 0:
            more = False
        i += 1
        
    return cyc

def findOdd(nodes):
    nodeStats = {}
    odd = []
    for node in nodes.keys():
        nodeStats[node] = [0,0]
        
    for node,outs in nodes.iteritems():
        nodeStats[node][1] = len(outs)
        for out in outs:
            try:
                nodeStats[out][0] += 1
            except KeyError:
                nodeStats[out] = [1,0]
    for node,stats in nodeStats.iteritems():
        if stats[0] != stats[1]:
            odd.append(node)
    if len(odd) > 3:
        exit()
    if len(odd) == 2:
        if nodeStats[odd[0]][1] == 0:
            finish = odd[0]
            start = odd[1]
        else:
            finish = odd[1]
            start = odd[0]
    else:
        start = nodes.keys()[0]
        finish = ''

    return start,finish

def eulerianPath(nodes):
    start,finish = findOdd(nodes)

    #print nodes
    f = True
    i = 0
    more = True
    last = []
    while more:
        if f:
            cyc,nodes = ecy(nodes,start)
            f = False
            #print '->'.join(cyc)
        else:
            try:
                start = cyc[i]
            except IndexError:
                more = False
            try:
                subcyc,nodes = ecy(nodes,start)
            except KeyError:
                i += 1
                continue
            if len(subcyc) > 1:
                if subcyc[-1] != finish:
                    #print 'before:','->'.join(cyc)
                    #print 'sub:','->'.join(subcyc)
                    cyc = cyc[:i] + subcyc + cyc[i+1:]
                    #print 'after:','->'.join(cyc)
                else:
                    j = 0
                    last = deepcopy(subcyc)
                    start = last[0]
                    atLast = False
                    while not atLast:
                        subcyc,nodes = ecy(nodes,start)
                        if len(subcyc) > 1:
                            last = last[:j] + subcyc + last[j+1:]
                        j += 1
                        if j == len(last) - 1:
                            atLast = True
                        
        if len(nodes) == 0:
            more = False
        i += 1
    cyc = cyc + last
        
    return cyc

def getEdge(n1,n2):
    edge = n1 + prefix(n2)
    return edge

def createBinaryMers(k):
    dec = int(math.pow(2,k))
    bmers = []
    unibmers = []
    for i in range(0,dec):
        dec = i
        remainders = []
        binary = []
        while dec >=1:
            remainders.append(dec%2)
            dec = dec/2
        for unit in reversed(remainders):
            binary.append(unit)
        bmers.append(''.join(map(str,binary)))

    for bmer in bmers:
        while len(bmer) < k:
            bmer = '0' + bmer
        unibmers.append(bmer)
    return unibmers


ins = open(sys.argv[1]).read().strip().split()

k = int(ins[0])
d = int(ins[1])
edgePairs = ins[2:]

nodes = deBrujnPaired(edgePairs)
path = eulerianPath(nodes)

fir = path[0].split('|')
fp = fir[0]
fs = fir[1]

precomp = fp
sufcomp = fs

for i in range(1,len(path)):
    ps = path[i].split('|')
    pre = ps[0]
    suf = ps[1]
    precomp += pre[-1]
    sufcomp += suf[-1]

#print precomp
#print sufcomp

print precomp[0:k+d]+sufcomp
#print recomp[0:len(recomp)-(k-1)]
        



    
