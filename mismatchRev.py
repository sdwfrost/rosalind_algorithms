import sys

# mismatchCheck takes a pattern, what you want to test against, and allowed misses.
# checks each character in the pattern against corresponding char in 'check'.
# adds up how many misses are found, and returns true or false depending on if
# allowed number of misses is exceeded or not.
def mismatchCheck(pattern, check,misses):
    match = False
    misCount = 0
    for i in range(len(pattern)):
        if check[i] != pattern[i]:
            misCount += 1
    if misCount <= misses:
        match = True
    return match
            
# approxMatch takes patter, the full sequence (and length), and number of allowed misses
# checks the pattern against every possible word in the sequence
def approxMatch(pattern,sequence,seqLength,misses):
    patternLength = len(pattern)
    mismatch = False
    count= 0
    for i in range(seqLength):
        check = sequence[i:patternLength+i]
        if len(check) == len(pattern):
            mismatch = mismatchCheck(pattern,check,misses)
            if mismatch:
                count += 1
    return count

def complement(s):
    complD = {'A':'T','C':'G','G':'C','T':'A'}
    return ''.join(map(complD.get,s))
    

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

revcomp = ''.join(reversed(complement(sequence)))

#Put all possible kmers in list
for i in range(seqLength-k+1):
    if not revcomp[i:i+k] in kmers:
        kmers[revcomp[i:i+k]] = 0
        kmersInString[revcomp[i:i+k]] = 1
    else:
        kmersInString[revcomp[i:i+k]] += 1
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
