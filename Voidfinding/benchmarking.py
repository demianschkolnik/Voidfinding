import numpy as np
import cProfile

def distance(x1,y1,x2,y2):
    "distance between (x1,y1) and (x2,y2)"
    deltaXSquare = (x1-x2)**2
    deltaYSquare = (y1-y2)**2
    return (deltaXSquare+deltaYSquare) ** (0.5)


def test(file):
    epsilon    = 100                #epsilon is the distance to check for neighbours
    k          = 4                  #k is the number on the epsilon-neighborhood criterion

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

    # Ids
    center = []
    outlier = []
    border = []

    #check for center objects.
    for i in range(0,l):
        nrNeigh = 0
        for j in range(0,l):
            if (M[i,j] <= epsilon) and i != j:
                nrNeigh += 1
        if nrNeigh >= k:
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


if __name__ == '__main__':
    import timeit


    files = ['20irr2d_1024.dat','20irr2d_2048.dat','20irr2d_4096.dat','20irr2d_8192.dat','20irr2d_16384.dat',
             '20irr2d_32768.dat','20irr2d_65536.dat','20irr2d_131072.dat','20irr2d_262144.dat']

    file = open('results.txt', 'w')



    for file in files:
        run = "test(\"Data/"+file+"\")"
        result = (timeit.timeit(run, setup="from __main__ import test",number=1))
        print(result)
        file.write(result + '\n')
    file.close()