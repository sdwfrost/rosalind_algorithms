import sys
            
def neighbors(s, d):
    l = []
    if d==0 or len(s)==0:
        return[s]
    for n in 'ACGT':
        d1 = d-1      
        if n==s[0]:
            d1 = d
        for m in neighbors(s[1:], d1):
            l.append(n + m)
    return l

inputfile = open(sys.argv[1]).read().split()
sequence = inputfile[0].rstrip()
k = int(inputfile[1])
d = int(inputfile[2])

# 'counts' and 'kMers' are parallel lists
seqLength = len(sequence)
kmers = {}
kmersSet = set()
kmersToAdd = set()

kmersInString= {}

#Put all possible kmers in list
for i in range(seqLength):
    if len(sequence[i:i+k]) == k:
        if not sequence[i:i+k] in kmers:
            kmers[sequence[i:i+k]] = 0
            kmersInString[sequence[i:i+k]] = 1
        else:
            kmersInString[sequence[i:i+k]] += 1

for kmer in kmersInString.keys():
    mers = neighbors(kmer,d)
    for mer in mers:
        if mer in kmers:
            kmers[mer] += kmersInString[kmer]
        else:
            kmers[mer] = kmersInString[kmer]

outString = ''
highestCount = 0

#Find highest occuring
for kmer,count in kmers.items():
    if count > highestCount:
        outString = kmer
        highestCount = count
    elif count == highestCount:
        outString = outString + ' ' + kmer

print outString
        


