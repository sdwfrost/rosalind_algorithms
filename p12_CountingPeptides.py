import sys

mass = int(open(sys.argv[1]).read())

def massCount(mass):
    mw = {'A':71,'C':103,'D':115,'E':129,'F':147,'G':57,'H':137,'I':113,'K':128,'L':113,'M':131,'N':114,'P':97,'Q':128,'R':156,'S':87,'T':101,'V':99,'W':186,'Y':163}

    ws = set()
    for w in mw.values():
        ws.add(w)
    counts = {0:1}
    
    for i in range(1,mass + 1):
        #addedws = []
        for w in ws:
            if (i-w) in counts: #and not (i-w) in addedws:
                if i in counts:
                    counts[i] += counts[(i-w)]
                    #addedws.append(i-w)
                else:
                    counts[i] = counts[(i-w)]
                    #addedws.append(i-w)
    return counts
            
count = massCount(mass)

print count[mass]



        
