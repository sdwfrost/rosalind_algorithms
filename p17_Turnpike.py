import sys

def tphelp(D,A,pointToAdd):
    removed = []
    distsGood = True
    for point in A:
        if point > pointToAdd:
            dist = point - pointToAdd
        else:
            dist = pointToAdd - point
        if dist in D:
            D.remove(dist)
            removed.append(dist)
        else:
            distsGood = False
            break
    if not distsGood:
        for r in removed:
            D.append(r)
        return False

    A.append(pointToAdd)

    if turnpike(D,A):
        return True
    else:
        A.remove(pointToAdd)
        for r in removed:
            D.append(r)
        return False
        

def turnpike(D,A):
    if len(D) == 0:
        return True
    distMax = max(D)
    low = max(A)-distMax

    if tphelp(D,A,distMax) or tphelp(D,A,low):
        return True
    else:
        return False
        

    
    


D = open(sys.argv[1]).read().split()
D = map(int,D)

numItems = D.count(0)
A = [0,max(D)]
D = filter(lambda x: x > 0, D)
D.remove(max(D))

turnpike(D,A)
for a in sorted(A):
    print a,



