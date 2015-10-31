import sys

def genSpectrum(peptide,cy):
    pepLen = len(peptide)
    mw = {'A':71,'C':103,'D':115,'E':129,'F':147,'G':57,'H':137,'I':113,'K':128,'L':113,'M':131,'N':114,'P':97,'Q':128,'R':156,'S':87,'T':101,'V':99,'W':186,'Y':163}
    totalMass = 0
    for char in peptide:
        totalMass += mw[char]
    if cy:
        peptide = peptide + peptide
    totals = [0]
    totalLen = len(peptide)
    for i in range(pepLen):
        for j in range(1,pepLen):
            total = 0
            sub = ''
            if (j + i) < totalLen:
                sub = peptide[i:i+j]
            for char in sub:
                total += mw[char]
            if total != 0:
                totals.append(total)
    totals.append(totalMass)
    return totals

    
peptide = open(sys.argv[1]).read().strip()

totals = genSpectrum(peptide,False)

for weight in sorted(totals):
    print weight,
    

