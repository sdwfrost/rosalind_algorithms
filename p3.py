import sys


inputfile = open(sys.argv[1]).read().split()
pattern = inputfile[0]
sequence = inputfile[1]

seqLength = len(sequence)
patternLength = len(pattern)
count = 0
locations = ''
for i in range(seqLength):
    check = sequence[i:patternLength+i]
    if check == pattern:
        locations += str(i) + ' '

print locations
