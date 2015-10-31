import sys

def reverseComplement(seq):
    seq = seq.upper()
    compl_dict = {'A':'T', 'T':'A', 'C':'G', 'G':'C'}
    rc_seq = ''
    for nuc in seq[::-1]:
        rc_seq += compl_dict.get(nuc,nuc)
    return rc_seq

def translateCodon(codon,codons):
    if codon in codons:
        return codons[codon]
    else:
        return 'X'

def findSubString(peptide,seq,reverse,codons):
    substrings = []
    look = True
    position = 0
    aaseq = ''
    length = len(peptide) * 3
    for i in range(3):
        for j in range(i,seqlen,3):
            codon = seq[j:j+3]
            aa = translateCodon(codon,codons)
            aaseq  += aa

        #Flag to continue looking in while loop
        look = True

        #Flag for first item being looked at
        first = True
        
        while look:
            if not first:
                position = aaseq.find(peptide,(position+1))
            else:
                position = aaseq.find(peptide)
                first = False
            #get sequence using position of amino acid in sequence
            if position >=0:
                start = 3*position + i
                if not reverse:
                    substrings.append(seq[start:(start+length)])
                else:
                    revcodons = seq[start:(start+length)]
                    revcodons = reverseComplement(revcodons)
                    substrings.append(revcodons)
            else:
                look = False
        aaseq = ''
    return substrings

def findAllSubstrings(peptide,seq,codons):
    forward = findSubString(peptide,seq,False,codons)
    revComp = reverseComplement(seq)
    backward = findSubString(peptide,revComp,True,codons)
    substrings = forward + backward
    return substrings

codonFile = open(sys.argv[1])
sf = open(sys.argv[2])

dataSet = sf.read().split()
sf.close()

seq = dataSet[0]
peptide = dataSet[1]

#seq = seq.replace('T','U')

data = {}
for l in codonFile:
    sl = l.split()
    key = sl[0]
    value = sl[2]
    data[key] = value
codonFile.close()

b1 = data['Base1']#.replace('T','U')
b2 = data['Base2']#.replace('T','U')
b3 = data['Base3']#.replace('T','U')
aa = data['AAs']
st = data['Starts']

codons = {}
init = {}
n = len(aa)
seqlen = len(seq)
aaseq = ''
startCodon = False

for i in range(n):
    codon = b1[i] + b2[i] + b3[i]
    codons[codon] = aa[i]
    init[codon] = (st[i] == 'M')

substrings = findAllSubstrings(peptide,seq,codons)

for sub in substrings:
    print sub


