import numpy as np

def distance(x1,y1,x2,y2):
    "distance between (x1,y1) and (x2,y2)"
    deltaXSquare = (x1-x2)**2
    deltaYSquare = (y1-y2)**2
    return (deltaXSquare+deltaYSquare) ** (0.5)


epsilon    = 100                #epsilon is the distance to check for neighbours
k          = 4                  #k is the number on the epsilon-neighborhood criterion
file       = 'Data/data1.dat'   #File to be read






#Parse de read data
f = open(file, 'r')
i = 0
first = 0
for r in f:
    if first == 0:
        dimensions = int(r)
        first += 1
    elif first == 1:
        l = int(r)
        first += 1
        raw = np.zeros((l,2))
    else:
        row = r.split()
        raw[i,0] = float(row[0])
        raw[i,1] = float(row[1])
        i += 1



M = np.zeros((l, l))

#Filling distance Matrix M
for i in range(0,l):
    for j in range(0,i):
        dist = distance(raw[i,0],raw[i,1],raw[j,0],raw[j,0])
        M[i,j] = dist
        M[j,i] = dist

resultsO = np.zeros((21,11),int)
resultsC = np.zeros((21,11),int)
resultsB = np.zeros((21,11),int)

aux = 50
for d in range(1,21):
    resultsO[d,0] = aux
    resultsC[d, 0] = aux
    resultsB[d, 0] = aux
    aux += 50

aux = 1
for d in range(1,11):
    resultsO[0,d] = aux
    resultsC[0, d] = aux
    resultsB[0, d] = aux
    aux += 1

count = 0
for epsI in range(1,21):
    for kvI in range(1,11):
        count += 1
        eps = resultsC[epsI,0]
        kv = resultsC[0,kvI]
        print("calculating for eps=" + str(eps) + " and k=" + str(kv) + " " + str(count) + "/200")
        # Ids
        center = []
        outlier = []
        border = []

        #check for center objects.
        for i in range(0,l):
            nrNeigh = 0
            for j in range(0,l):
                if (M[i,j] <= eps) and i != j:
                    nrNeigh += 1
            if nrNeigh >= kv:
                center.append(i)
            else:
                outlier.append(i)

        #Move candidates from outlier to border
        for cand in outlier:
            wasBorder = False
            for c in center:
                if M[cand,c] <= epsilon:
                    border.append(cand)
                    wasBorder = True
                    break
            if wasBorder:
                outlier.remove(cand)
        resultsO[epsI,kvI] = len(outlier)
        resultsC[epsI, kvI] = len(center)
        resultsB[epsI, kvI] = len(border)


np.savetxt("resultsO.csv", resultsO, delimiter=",")
np.savetxt("resultsC.csv", resultsC, delimiter=",")
np.savetxt("resultsB.csv", resultsB, delimiter=",")