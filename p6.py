import sys

def mismatchCheck(pattern, check,misses):
    match = False
    misCount = 0
    for i in range(len(pattern)):
        if check[i] != pattern[i]:
            misCount += 1
    if misCount <= misses:
        match = True
    return match
            
    
def approxMatch(pattern,sequence,seqLength,misses):
    patternLength = len(pattern)
    matchIndex = ''
    mismatch = False
    for i in range(seqLength):
        check = sequence[i:patternLength+i]
        if len(check) == len(pattern):
            mismatch = mismatchCheck(pattern,check,misses)
        if mismatch:
            matchIndex += str(i) + ' '
    return matchIndex
            
            
        

inputfile = open(sys.argv[1]).read().split()
pattern = inputfile[0].rstrip()
sequence = inputfile[1].rstrip()
misses = int(inputfile[2])

seqLength = len(sequence)

print approxMatch(pattern,sequence,seqLength,misses)

