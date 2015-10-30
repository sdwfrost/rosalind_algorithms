import sys

def DPChange(money,coins):
    minNums = {0:0}

    for i in range(1,money+1):
        minNums[i] = 999999999
        for coin in coins:
            if i >= coin:
                if minNums[i-coin] + 1 < minNums[i]:
                    minNums[i] = minNums[i-coin] + 1
    #print minNums
    return minNums[money]

ins = open(sys.argv[1]).read().split()
money = int(ins[0])
coins = map(int,ins[1].split(','))

minCoins = DPChange(money,coins)
print minCoins