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
        second = ','.join(second)
        if second != '':
            dbNodes.append((node[0],second))
    return dbNodes



###############  Eulerian Cycle  #############################

def ecy(nodes,start):
    more = True
    cyc = []
    pos = start
    while more:
        cyc.append(pos)
        try:
            n = nodes[pos].pop()
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
                nodeStats[out] = [0,1]
    for node,stats in nodeStats.iteritems():
        if stats[0] != stats[1]:
            odd.append(node)
            if stats[0] == 0:
                finish = node
            else:
                start = node
    if len(odd) > 3:
        exit()
    return start,finish

def eulerianPath(nodes):
    start,finish = findOdd(nodes)
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
        
        

inNodes = open(sys.argv[1],'r').read().split('\n')
nodes = {}

for node in inNodes:
    if len(node) > 1:
        nd = node.split()
        choices = nd[2].split(',')
        nodes[nd[0]] = choices

print nodes
cycle = eulerianPath(nodes)

print '->'.join(cycle)




    









