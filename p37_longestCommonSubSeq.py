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
        

# These used for inputs to ny path
#down = ''.join(ins[ins.find('\n')+1:].split('-')[0]).split('\n')
#right = ''.join(ins[ins.find('\n')+1:].split('-')[1]).split('\n')


ins = open(sys.argv[1]).read().split()


s1 = ins[0]
s2 = ins[1]


backtrack = lcs(s1,s2)

##for a,back in backtrack.iteritems():
##    for c,b in back.iteritems():
##        print b,
##    print


out = []



outputLCS(backtrack,s1,len(s1),len(s2),out)



print ''.join(out)