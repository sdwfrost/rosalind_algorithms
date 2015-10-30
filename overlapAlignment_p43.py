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
        s[0][j] = j*-1
    for i in range(0,len(v)+1):
        s[i][0] = i*-1
    for i in range(1,len(v)+1):
        for j in range(1,len(w)+1):
            if v[i-1] == w[j-1]:
                s[i][j]=max((s[i-1][j]-1),(s[i][j-1]-1),(s[i-1][j-1]+1))
            else:
                s[i][j]=max((s[i-1][j]-1),(s[i][j-1]-1),(s[i-1][j-1]-1))

            if s[i][j] == s[i-1][j]-1:
                backtrack[i][j] = "down"
            elif s[i][j] == s[i][j-1]-1:
                backtrack[i][j] = "right"
            elif s[i][j] == (s[i-1][j-1] + 1) or (s[i][j] == (s[i-1][j-1]-1)):
                backtrack[i][j] = "diag"


    #print s 
    for j in range(len(backtrack)):
        del backtrack[j][0]
    del backtrack[0]
    return backtrack,s

def overlapAlign(v,w):
    s = [[0for j in range(len(w)+1)] for i in range(len(v)+1)]
    backtrack = [[0 for j in range(len(w)+1)] for i in range(len(v)+1)]

    for i in range(1,len(v)+1):
        for j in range(1,len(w)+1):
            scores = [s[i-1][j] - 2,s[i][j-1] - 2 ,s[i-1][j-1] + [-2,1][v[i-1]==w[j-1]]]
            s[i][j] = max(scores)
            backtrack[i][j] = scores.index(s[i][j])

   # for b in s:
    #    print b

    i = len(v)
    j = max(enumerate([s[i][col] for col in range(len(w))]),key=lambda x: x[1])[0]
    max_score = str(s[i][j])

    v_align = v[:i]
    w_align = w[:j]

    indels = lambda word, i: word[:i] + '-' + word[i:]

    while i*j != 0:
        if backtrack[i][j] == 0:
            i -= 1
            w_align = indels(w_align,j)
        elif backtrack[i][j] == 1:
            j -= 1
            v_align = indels(v_align,i)
        elif backtrack[i][j] == 2:
            i -= 1
            j -= 1
    v_align = v_align[i:]

    print max_score
    print v_align
    print w_align

    
def fittingAlign(s1,s2):
    s = [[0for j in range(len(s2)+1)] for i in range(len(s1)+1)]
    backtrack = [[0 for j in range(len(s2)+1)] for i in range(len(s1)+1)]



    for i in range(1,len(s1)+1):
        for j in range(1,len(s2)+1):
            scores = [s[i-1][j]-1,s[i][j-1] -1,s[i-1][j-1] + [-1,1][s1[i-1]==s2[j-1]]]
            s[i][j] = max(scores)
            backtrack[i][j] = scores.index(s[i][j])

    j = len(s2)
    i = max(enumerate([s[row][j] for row in range(len(s2),len(s1))]),key=lambda x: x[1])[0] + len(s2)
    max_score = str(s[i][j])

    s1a,s2a = s1[:i],s2[:j]
    
    indels = lambda word, i: word[:i] + '-' + word[i:]

    while i*j != 0:
        if backtrack[i][j] == 0:
            i -= 1
            s2a = indels(s2a,j)
        elif backtrack[i][j] == 1:
            j -= 1
            s1a = indels(s1a,i)
        elif backtrack[i][j] == 2:
            i -= 1
            j -= 1
    s1a = s1a[i:]
##
##    for a in backtrack:
##        print a
        #for b in a:
            #print str(b),
    #print

    print max_score
    print s1a
    print s2a
    
    

def outputLCSLong(backtrack,v,i,j,out):
    done = False
    printed = False
    ilast = i+1
    jlast = j+1
    while not done:
        x = i
        y = j
        if x == 0:
            x = 1
        if y == 0:
            y = 1
        if backtrack[x][y] == 'down':
            out.append('-')
            if i != 0:
                i = i-1
        elif backtrack[x][y] == 'right':
            out.append(v[j-1])
            if j != 0:
                j = j-1
        else:
            if j > 0:
                out.append(v[j-1])
            else:
                out.append('-')
            if i != 0:
                i = i-1
            if j != 0:
                j = j-1
        if i == 0 and j == 0:
            done = True
    return out
def outputLCSShort(backtrack,v,i,j,out):
    done = False
    printed = False
    
    while not done:
        x = i
        y = j
        if x == 0:
            x = 1
        if y == 0:
            y = 1
        if backtrack[x][y] == 'down':
            out.append(v[i-1])
            if i != 0:
                i = i-1
        elif backtrack[x][y] == 'right':
            out.append('-')
            if j != 0:
                j = j-1
        else:
            if i > 0:
                out.append(v[i-1])
            else:
                out.append('-')
            if i != 0:
                i = i-1
            if j != 0:
                j = j-1
        if i == 0 and j == 0:
            done = True
    return out
            
        

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

#fittingAlign(s1,s2)
overlapAlign(s1,s2)

##if len(s2) < len(s1):
##    stemp = s1
##    s1=s2
##    s2=stemp
##
##highScore = -1000000
##out1 = 'osoadfasd'
##out2 = 'asdfasdf'
##triedsubs = set()
##for i in range(len(s2)+1):
##    #print 'i',i
##    for j in range(len(s1)+10):
##        #print 'j',j
##        sub = s2[j:i+j]
##        if i+j-1 < len(s2) and len(sub) >= len(s1)+10 and sub not in triedsubs:
##            backtrack,s = lcs(s1,sub)
##            triedsubs.add(sub)
##            score = s[len(s1)][len(sub)]
##            if score > highScore:
##                highScore = score
##                print score
##                out = []
##                outputLCSLong(backtrack,sub,len(s1),len(sub),out)
##                out1 = out
##                print ''.join(reversed(out1))
##                out1 = out
##                out = []
##                outputLCSShort(backtrack,s1,len(s1),len(sub),out)
##                out2 = out
##                print ''.join(reversed(out2))
##            
##            
##        


# this prints backtrack or s nicely (isn't nice with large inputs)
##for a,back in backtrack.iteritems():
##    for c,b in back.iteritems():
##        print str(b),
##    print
##
##print highScore
##print ''.join(reversed(out1))
##print ''.join(reversed(out2))