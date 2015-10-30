import sys

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
    #CONVENTION - Index of out dict (lenghts) corresponds to collumn
    #Index of inner dict corresponds to row
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
    #print lengths
    return lengths[m][n]

ins = open(sys.argv[1]).read()
n = int(ins[0:ins.find(' ')])
m = int(ins[ins.find(' ') + 1:ins.find('\n')])

down = ''.join(ins[ins.find('\n')+1:].split('-')[0]).split('\n')
right = ''.join(ins[ins.find('\n')+1:].split('-')[1]).split('\n')

down = down[0:len(down)-1]
right = right[1:len(right)-1]

length = longestPathTourist(n,m,down,right)

print length