import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import Delaunay
import plotDelaunay

# Se necesita fijar dos parámetros, una distancia epsilon y un número de
# vecinos k. Dados estos parámetros, las estrellas se clasifican en tres
# tipos:
#
# - Tipo centro: son las estrellas que tienen a una distancia <= epsilon a k
# o más estrellas vecinas.
#
# - Tipo borde: son las estrellas que tienen a una distancia <= epsilon una
# estrella de tipo centro, pero que no cumplen con la condición para ser de
# tipo centro.
#
# - Tipo outlier: las estrellas que no son ni centro ni borde.
#
# Luego, las estrellas de tipo borde serían candidatos a ser parte de la
# frontera a un vacío. Hay que pensar aún cómo construir las "murallas de
# los vacíos". Una idea inicial sería hacer una triangulación y luego marcar
# las aristas entre estrellas tipo borde, para definir los vacío.

def distance(x1,y1,x2,y2):
    "distance between (x1,y1) and (x2,y2)"
    deltaXSquare = (x1-x2)**2
    deltaYSquare = (y1-y2)**2
    return (deltaXSquare+deltaYSquare) ** (0.5)


epsilon    = 50                #epsilon is the distance to check for neighbours
k          = 4                  #k is the number on the epsilon-neighborhood criterion
file       = 'Data/20irr2d_1024.dat'   #File to be read
plotPoints = False              #Plot the points?
plotDelau  = True               #Plot Delaunay?


if plotPoints:
    plt.plotfile('data1.dat', delimiter=' ', cols=(0, 1),
             names=('col1', 'col2'),linestyle="", marker='.')
    plt.show()



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

#Ids
center = []
outlier = []
border = []

centerPointsPython = []
outlierPointsPython = []
borderPointsPython = []

#check for center objects.
for i in range(0,l):
    nrNeigh = 0
    for j in range(0,l):
        if (M[i,j] <= epsilon) and i != j:
            nrNeigh += 1
    if nrNeigh >= k:
        centerPointsPython.append(raw[i].tolist())
        center.append(i)
    else:
        outlier.append(i)
        outlierPointsPython.append(raw[i].tolist())

#Move candidates from outlier to border
for cand in outlier:
    wasBorder = False
    for c in center:
        if M[cand,c] <= epsilon:
            border.append(cand)
            borderPointsPython.append(raw[cand].tolist())
            wasBorder = True
            break
    if wasBorder:
        outlier.remove(cand)
        outlierPointsPython.remove(raw[cand].tolist())


if plotDelau :
    plotDelaunay.plot(centerPointsPython,outlierPointsPython,borderPointsPython,raw,epsilon)

