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
        s[0][j] = j*-5
    for i in range(0,len(v)+1):
        s[i][0] = i*-5
    for i in range(1,len(v)+1):
        for j in range(1,len(w)+1):
            s[i][j]=max((s[i-1][j]-5),(s[i][j-1]-5),(s[i-1][j-1]+score[v[i-1]][w[j-1]]))

            if s[i][j] == s[i-1][j]-5:
                backtrack[i][j] = "down"
            elif s[i][j] == s[i][j-1]-5:
                backtrack[i][j] = "right"
            elif s[i][j] == (s[i-1][j-1] + score[v[i-1]][w[j-1]]) or (s[i][j] == (s[i-1][j-1]+score[v[i-1]][w[j-1]])):
                if v[i-1] == w [j-1]:
                    backtrack[i][j] = "diag"
                else:
                    backtrack[i][j] = 'miss'


    #print s 
    for j in range(len(backtrack)):
        del backtrack[j][0]
    del backtrack[0]
    return backtrack,s

def calcEdit1(backtrack,i,j):
    done = False
    editcount = 0

    while not done:
        x = i
        y = j
        if i == 0:
            x = 1
        if j == 0:
            y = 1
        if backtrack[x][y] != 'diag':
            editcount += 1
            if backtrack[x][y] == 'down':
                if i != 0:
                    i = i-1
                else:
                    j = j - 1
            elif backtrack[x][y] == 'right':
                if j != 0:
                    j = j-1
                else:
                    i = i - 1
            elif backtrack[x][y] == 'miss':
                if i != 0:
                    i = i-1
                if j != 0:
                    j = j-1
        else:
            if i != 0:
                i = i-1
            if j != 0:
                j = j-1

        if i == 0 and j == 0:
            done = True
    return editcount
            

def calcEdit(s1,s2):
    d = [[0 for x in range(len(s2))] for x in range(len(s1))]

    for i in range(len(s1)):
        d[i][0] = i
    for j in range(len(s2)):
        d[0][j] = j

    if s1[0] != s2[0]:
        d[0][0] = 1
    
    for j in range(1,len(s2)):
        for i in range(1,len(s1)):
            if s1[i] == s2[j]:
                d[i][j] = d[i-1][j-1]
            else:
                d[i][j] = min(
                    d[i-1][j] + 1,
                    d[i][j-1] + 1,
                    d[i-1][j-1] + 1)
##    for row in d:
##        print row
    if s1[0] != s2[0]:
        x = 1
    else:
        x = 0
    return d[len(s1)-1][len(s2)-1] + x
    
def outputLCSLong(backtrack,v,i,j,out):
    done = False
    printed = False
    editcount = 0
    while not done:
        x = i
        y = j
        if x == 0:
            x = 1
        if y == 0:
            y = 1
        if backtrack[x][y] == 'down':
            editcount += 1
            out.append('-')
            if i != 0:
                i = i-1
        elif backtrack[x][y] == 'right':
            editcount += 1
            out.append(v[j-1])
            if j != 0:
                j = j-1
        else:
            if backtrack[x][y] == 'miss':
                editcount += 1
            if j > 0:
                out.append(v[j-1])
            else:
                editcount += 1
                out.append('-')
 
            if i != 0:
                i = i-1
            if j != 0:
                j = j-1
        if i == 0 and j == 0:
            done = True
    return editcount
def outputLCSShort(backtrack,v,i,j,out):
    done = False
    printed = False
    editcount = 0
    while not done:
        x = i
        y = j
        if x == 0:
            x = 1
        if y == 0:
            y = 1
        if backtrack[x][y] == 'down':
            out.append(v[i-1])
            editcount+=1
            if i != 0:
                i = i-1
        elif backtrack[x][y] == 'right':
            out.append('-')
            editcount += 1
            if j != 0:
                j = j-1
        else:
            if backtrack[x][y] == 'miss':
                editcount +=1
                #print 'missing'
            if i > 0:
                out.append(v[i-1])
            else:
                editcount += 1
                out.append('-')
               
            if i != 0:
                i = i-1
            if j != 0:
                j = j-1
        if i == 0 and j == 0:
            done = True
    return editcount
        

def outputLCS(backtrack,v,i,j,out,longer,printed):
    if i == 0:
        while j > 0:
            if longer:
                out.append('-')
            j = j-1
            
        return
    if j == 0:
        while i >0:
            if not longer:
                out.append('-')
            i = i-1
            
        return
            
        
    if backtrack[i][j] == 'down':
        outputLCS(backtrack,v,i-1,j,out,longer,printed)
        if not longer:
            out.append('-')
        elif not printed :
            out.append(v[i-1])
        
    elif backtrack[i][j] == 'right':
        outputLCS(backtrack,v,i,j-1,out,longer,printed)
        if longer:
            out.append('-')
        elif not printed:
            out.append(v[i-1])                    
    else:
        printed = False
        outputLCS(backtrack,v,i-1,j-1,out,longer,printed)
        out.append(v[i-1])
        
        

# These used for inputs to ny path
#down = ''.join(ins[ins.find('\n')+1:].split('-')[0]).split('\n')
#right = ''.join(ins[ins.find('\n')+1:].split('-')[1]).split('\n')


ins = open(sys.argv[1]).read().split()

matrix = open('blosum62.txt').read().split('\n')[1:]

mapping = {'A':0,'C':1,'D':2,'E':3,'F':4,'G':5,'H':6,'I':7,'K':8,'L':9,'M':10,'N':11,'P':12,'Q':13,'R':14,'S':15,'T':16,'V':17,'W':18,'Y':19}
mapping = {v: k for k, v in mapping.items()}
score = {}
for i in range(len(matrix)):
    splitrow = matrix[i].split()[1:]
    for j in range(len(splitrow)):
        score[mapping[i]]= {}
    for j in range(len(splitrow)):
        score[mapping[i]][mapping[j]] = int(splitrow[j])
    
s1 = ins[0]
s2 = ins[1]

if len(s2) < len(s1):
    stemp = s1
    s1=s2
    s2=stemp

#backtrack,s = lcs(s1,s2)

# this prints backtrack or s nicely (isn't nice with large inputs)
##for a,back in backtrack.iteritems():
##    for c,b in back.iteritems():
##        print str(b)+'\t',
##    print

    
##maxs = -2
##maxa = ''
##maxc = ''
##for a,back in s.iteritems():
##    for c,b in back.iteritems():
##        if b > maxs:
##            maxs = b
##            maxa = a
##            maxc = c
##
##
##out = []

maxEditCounts = calcEdit(s1,s2)

###print maxEditCounts
###print ''.join(reversed(out))
##
##out = []
##ec = calcEdit(backtrack,len(s1),len(s2))
###print ec
###print ''.join(reversed(out))
##if ec > maxEditCounts:
##    maxEditCounts = ec

print maxEditCounts