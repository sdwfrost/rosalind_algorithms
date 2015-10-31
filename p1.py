# Read in string

stringInputFile = open('rosalind_input.txt', 'r')
dnaString = stringInputFile.read().rstrip()
stringInputFile.close()

# init dict, get k (unsure what rosalind input will be exactly, otherwise would just read k

kMerDict = {}
kValue = int(raw_input("Enter k: "))

# for each character, when there exists a k-mer at that point, add kMer count to dict
# kMerDict is keeping a running total of each kmer. if kmer is new, it creates it in dict
# if kmer already found once, it adds 1 to its value.

for i in range(len(dnaString)):
    if len(dnaString[i:i+kValue]) == kValue:
        if dnaString[i:i+kValue] in kMerDict:
            kMerDict[dnaString[i:i+kValue]] += 1
        else:
            kMerDict[dnaString[i:i+kValue]] = 1

# Now find highest value in dict and print it out to file
outString = ''
highestCount = 0

for kMer,count in kMerDict.iteritems():
    if count > highestCount:
        outString = kMer
        highestCount = count
    elif count == highestCount:
        outString = outString + ' ' + kMer

print outString
