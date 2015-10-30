import sys

sys.setrecursionlimit(99999999)

def DPChange(money,coins):
    minNums = {0:0}

    for i in range(1,money+1):
        minNums[i] = 999999999
        for coin in coins:
            if i >= coin:
                if minNums[i-coin] + 1 < minNums[i]:
                    minNums[i] = minNums[i-coin] + 1
    return minNums[money]


def longestPathTourist(n,m,down,right):
    lengths = {}
    lengths[0] = {0:0}
    downs = {}
    rights = {}

########### Make data usable (dictionary) ############
    
    for i,d in enumerate(down):
        downs[i] = []
        for j in d.split():
            downs[i].append(int(j))

    for i,r in enumerate(right):
        rights[i] = []
        for j in r.split():
            rights[i].append(int(j))
            
######################################################

    for i in range(1,n+1):
        lengths[0][i] = lengths[0][i-1] + downs[i-1][0]
    
    for j in range(1,m+1):
        lengths[j] = {0:0}
        lengths[j][0] = lengths[j-1][0] + rights[0][j-1]
        
    for i in range(1,n+1):
        for j in range(1,m+1):
            lengths[j][i] = max(lengths[j][i-1] + downs[i-1][j],lengths[j-1][i] + rights[i][j-1])

    return lengths[m][n]

def lcs(v,w):
    s = {}
    backtrack = {}
    for i in range(0,len(v)+1):
        s[i] = {0:0}
        backtrack[i] = {0:0}
    for j in range(0,len(w)+1):
        s[0][j] = 0

    for i in range(1,len(v)+1):
        for j in range(1,len(w)+1):
            if v[i-1] == w[j-1]:
                s[i][j]=max(s[i-1][j],s[i][j-1],(s[i-1][j-1]+1))
            else:
                s[i][j]=max(s[i-1][j],s[i][j-1])

            if s[i][j] == s[i-1][j]:
                backtrack[i][j] = "down"
            elif s[i][j] == s[i][j-1]:
                backtrack[i][j] = "right"
            elif s[i][j] == (s[i-1][j-1] + 1):
                backtrack[i][j] = "diag"


    #print s 
    for j in range(len(backtrack)):
        del backtrack[j][0]
    del backtrack[0]
    return backtrack

def outputLCS(backtrack,v,i,j,out):
    if i == 0 or j == 0:
        return
    if backtrack[i][j] == 'down':
        outputLCS(backtrack,v,i-1,j,out)
    elif backtrack[i][j] == 'right':
        outputLCS(backtrack,v,i,j-1,out)
    else:
        outputLCS(backtrack,v,i-1,j-1,out)
        out.append(v[i-1])

def makeEdges(al):
    edges = {}
    for e in al:
        parts = e.split('->')
        dn = int(parts[1].split(':')[0])
        w = int(parts[1].split(':')[1])
        if int(parts[0]) in edges:
            edges[int(parts[0])].append((dn,w))
        else:
            edges[int(parts[0])]= [(dn,w)]
    return edges

def makePoint(edges):
    pointlist = {}
    for n,edgelist in edges.iteritems():
        for edge in edgelist:
            if edge[0] in pointlist:
                pointlist[edge[0]].append(n)
            else:
                pointlist[edge[0]] = [n]
    return pointlist

def scoreNode(edges,g,pos,backtrack,pointlist,sink):
    nlist = []
    if pos == sink:
        return []
    try:
        for edge in edges[pos]:
            nlist.append(edge[0])
            pointers = pointlist[edge[0]]
            if edge[0] not in g:
                maxW =-1000
            else:
                maxW = g[edge[0]]
            for point in pointers:
                nw = g[pos]+edge[1]
                if nw > maxW:
                    maxW = g[pos]+edge[1]
                    backtrack[edge[0]] = pos
                    g[edge[0]] = maxW
    except KeyError:
        return []

    return nlist
def longestDAG(source,sink,al):
    edges = makeEdges(al)
    pointlist = makePoint(edges)

    g = {source:0}
    backtrack = {}

    pos = source
    plist = scoreNode(edges,g,pos,backtrack,pointlist,sink)
    notDone = True
    while notDone:
        for pos in plist:
            newposlist = scoreNode(edges,g,pos,backtrack,pointlist,sink)
            if len(newposlist) == 0:
                notDone = False
        plist = newposlist

    return g,backtrack

def outLongDAG(backtrack,source,pos,path):
    if pos == source:
        path.append(pos)
        return
    path.append(pos)
    pos = backtrack[pos]
    outLongDAG(backtrack,source,pos,path)
        
    
        

# These used for inputs to ny path
#down = ''.join(ins[ins.find('\n')+1:].split('-')[0]).split('\n')
#right = ''.join(ins[ins.find('\n')+1:].split('-')[1]).split('\n')


ins = open(sys.argv[1]).read().split()
source = int(ins[0])
sink = int(ins[1])
al = ins[2:]
path = []
g,backtrack = longestDAG(source,sink,al)

print g[sink]
outLongDAG(backtrack,source,sink,path)
path = map(str,path)
print '->'.join(reversed(path))