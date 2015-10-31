def complement(nuc):
    if nuc == 'A': return 'T'
    elif nuc == 'C': return 'G'
    elif nuc == 'G': return 'C'
    elif nuc == 'T': return 'A'
    else: return nuc
    

# Read in string

stringInputFile = open('rosalind_1b.txt', 'r')
dnaString = stringInputFile.read().rstrip()
stringInputFile.close()

#complement dnaString
dnaRComplement = ''
for nuc in dnaString:
    dnaRComplement = complement(nuc) + dnaRComplement

#reverse

#dnaRComplement = dnaComplement[::-1]

outputFile = open('output.txt', 'w')
outputFile.write(dnaRComplement)
outputFile.close()
