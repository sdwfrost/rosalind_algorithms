import sys

codonFile = open(sys.argv[1])
sf = open(sys.argv[2])

seq = ''.join((sf.read()).split())
sf.close()

seq = seq.replace('T','U')

data = {}
for l in codonFile:
    sl = l.split()
    key = sl[0]
    value = sl[2]
    data[key] = value
codonFile.close()

b1 = data['Base1'].replace('T','U')
b2 = data['Base2'].replace('T','U')
b3 = data['Base3'].replace('T','U')
aa = data['AAs']
st = data['Starts']

codons = {}
init = {}
n = len(aa)
seqlen = len(seq)
aaseq = []
startCodon = False

for i in range(n):
    codon = b1[i] + b2[i] + b3[i]
    codons[codon] = aa[i]
    init[codon] = (st[i] == 'M')


for i in range(0,seqlen,3):
    codon = seq[i:i+3]
    aa = codons[codon]
    if aa == '*':
        break
    aaseq.append(aa)
    if i == 0:
        startCodon = init[codon]

print ''.join(aaseq)
