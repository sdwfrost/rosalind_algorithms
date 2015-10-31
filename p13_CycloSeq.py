import sys

def genSpectrum(peptide,cy,mw,totalWeight):
    pepLen = len(peptide)
    totalMass = 0
    for char in peptide:
        totalMass += mw[char]
    if totalMass == totalWeight:
        cy = True
    if cy:
        peptide = peptide + peptide
    totals = [0]
    totalLen = len(peptide)
    for i in range(pepLen):
        for j in range(1,pepLen):
            total = 0
            total = sum(map(mw.get,peptide[i:i+j]))
            if total != 0:
                totals.append(total)
    totals.append(totalMass)
    return totals

def checkSpec(peps,mw,spectrum):
    pepsToRemove = []
    done = False
    totalWeight = spectrum[-1]
    if len(peps) == 0:
        print 'nopeps'
    for pep in peps:
        spec = genSpectrum(pep,False,mw,totalWeight)
        subset = True
        for mass in spec:
            if not mass in spectrum:
                subset = False
                break
        if not subset:
            pepsToRemove.append(pep)
        else:
            if len(spectrum) == len(spec):
                done = True

    for pep in pepsToRemove:
            peps.remove(pep)
    
    return peps,done

def addAmino(peps,mw,count):
    pepToAdd = []
    for amino in mw.keys():
        for pep in peps:
            pepToAdd.append(pep + amino)
    peps.extend(pepToAdd)
    peps = filter(lambda x: len(x)==count+1,peps)
    return peps
            
N = sys.argv[1]
spectrum = open(sys.argv[2]).read().strip().split()
spectrum = map(int,spectrum)


mw1 = {'A':71,'C':103,'D':115,'E':129,'F':147,'G':57,'H':137,'I':113,'K':128,'L':113,'M':131,'N':114,'P':97,'Q':128,'R':156,'S':87,'T':101,'V':99,'W':186,'Y':163}
mw = {}
for key,value in mw1.iteritems():
    if value not in mw.values():
        mw[key] = value

peps = []
done = False
count = 1
for amino in mw.keys():
    peps.append(amino)


noMatch = False
while not done:
    peps = addAmino(peps,mw,count)
    peps,done = checkSpec(peps,mw,spectrum)
    if done == -1:
        done = True
        noMatch = True
    count +=1
if noMatch:
    print 'No matches'
    sys.exit(0)
outstr = ''
for pep in peps:
    for char in pep:
        outstr += str(mw[char]) + '-'
    outstr = outstr[0:len(outstr)-1]
    outstr += " "

outstr = ' '.join(set(outstr.split()))
print outstr
