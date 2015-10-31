import sys

sequence = ''.join(open(sys.argv[1]).read().split())

seqLength = len(sequence)

skew = range(seqLength+1)
skew[0] = 0


for i in range(seqLength):
    if sequence[i] == 'C':
        skew[i+1] = skew[i]-1
    elif sequence[i] == 'G':
        skew[i+1] = skew[i] + 1
    else:
        skew[i+1] = skew[i]

#minimum = str(skew.index(min(skew)))
minIndex = ''
minValue = 0
for i in range(len(skew)):
    if skew[i] < minValue:
        minValue = skew[i]
        minIndex = str(i)
    elif skew[i] == minValue:
        minIndex += ' ' + str(i)
print minIndex
