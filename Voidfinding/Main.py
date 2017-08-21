import matplotlib.pyplot as plt
import numpy as np
import plotPoints as pp

#from scipy.spatial import Delaunay
#import plotDelaunay

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

manualEpsilon = False #Manual epsilon or calculated
epsilon    = 200 #epsilon is the distance to check for neighbours
k          = 12 #k is the number on the epsilon-neighborhood criterion
file       = 'Data/20irr2d_1024.dat' #File to be read
plot = True #Plot?
plotNearestNeighbour = True #Plot lines to epsilon-neighbours?



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
       dist = distance(raw[i,0],raw[i,1],raw[j,0],raw[j,1])
       M[i,j] = dist
       M[j,i] = dist


#calculate epsilon depending on k: epsilon is de mean distance of the kth neighbour.
def epsilonForK(k,M,l):
    kNearest = []
    for i in range(0,l):
        kNearest.append(sorted(M[i])[k+1])
    return np.mean(kNearest)

if not manualEpsilon:
    epsilon = epsilonForK(k,M,l)

#Ids
center = []
outlier = []
candidates = []
border = []

centerPointsPython = []
outlierPointsPython = []
candidatesPointsPython = []
borderPointsPython = []

neighbourEdge_points = []
neighbour_edges = set()

def add_edge(i, j):
    """Add a line between the i-th and j-th points, if not in the list already"""
    if (i, j) in neighbour_edges or (j, i) in neighbour_edges:
        return
    neighbour_edges.add((i, j))
    neighbourEdge_points.append(raw[ [i, j] ])

#check for center objects.
for i in range(0,l):
   nrNeigh = 0
   for j in range(0,l):
       if (M[i,j] <= epsilon) and i != j:
           nrNeigh += 1
           if plotNearestNeighbour:
               add_edge(i,j)
   if nrNeigh >= k:
       centerPointsPython.append(raw[i].tolist())
       center.append(i)
   else:
       candidates.append(i)
       candidatesPointsPython.append(raw[i].tolist())

#Move candidates from outlier to border
for cand in candidates:
   wasBorder = False
   for c in center:
       if M[cand,c] <= epsilon:
           border.append(cand)
           borderPointsPython.append(raw[cand].tolist())
           wasBorder = True
           break
   if not wasBorder:
       outlier.append(cand)
       outlierPointsPython.append(raw[cand].tolist())

if plot:
    plotName = 'Data:' + file + ' | epsilon:' + str(epsilon) + ' | k:' + str(k)
    if plotNearestNeighbour:
        pp.plotWithEpsilonNeighbour(plotName, centerPointsPython, outlierPointsPython, borderPointsPython,neighbourEdge_points)
    else:
        pp.plot(plotName, centerPointsPython, outlierPointsPython, borderPointsPython)
