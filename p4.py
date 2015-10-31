import sys

def countPattern(pattern,sequence,seqLength,k):
    count = 0
    patternLength = len(pattern)
    if patternLength == k:        
        for i in range(seqLength):
            check = sequence[i:patternLength+i]
            if check == pattern:
                count += 1
        return count

def countPatternWhile(pattern,sequence,seqLength,k):
    count = 0
    patternLength = len(pattern)
    found = True
    index = 0
    if patternLength == k:
        while found:
            index = sequence.find(pattern, index+1)
            if index > 0:
                count+=1
            else:
                found = False
    return count
            
    
inputfile = open(sys.argv[1]).read().split()
sequence = inputfile[0].rstrip()
k = int(inputfile[1])
L = int(inputfile[2])
t = int(inputfile[3])

clumps = ''

seqLength = len(sequence)
#for loop for window, check pattern in window
count = 0
for i in range(seqLength):
    window = sequence[i:i+L].rstrip()
    for j in range(len(window)):
        pattern = window[j:j+k]
        count = countPatternWhile(pattern,window,L,k)
        if count >= t:
            if clumps.find(pattern) == -1:
                clumps += pattern + ' '

print clumps
    
