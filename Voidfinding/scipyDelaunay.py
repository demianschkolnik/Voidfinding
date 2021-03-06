import numpy as np
from scipy.spatial import Delaunay
import plotPoints as pp

manualEpsilon = False #Manual epsilon or calculated
epsilon    = 30 #epsilon is the distance to check for neighbours
k          = 9 #k is the number on the epsilon-neighborhood criterion
file       = 'Data/20irr2d_16384.dat' #File to be read
plot = True #Plot?
plotNearestNeighbour = True #Plot lines to epsilon-neighbours?
save = False #save as image?
printProgress = True #Print % of progress on console?

def distance(x1,y1,x2,y2):
   "distance between (x1,y1) and (x2,y2)"
   deltaXSquare = (x1-x2)**2
   deltaYSquare = (y1-y2)**2
   return (deltaXSquare+deltaYSquare) ** (0.5)

points = []

#Parse de read data
f = open(file, 'r')
i = 0
first = 0
points = []
for r in f:
   if first == 0:
       dimensions = int(r)
       first += 1
   elif first == 1:
       l = int(r)
       first += 1
       raw = np.zeros((l, 2))
   else:
       row = r.split()
       aux = []
       aux.append((float)(row[0]))
       aux.append((float)(row[1]))
       raw[i, 0] = float(row[0])
       raw[i, 1] = float(row[1])
       points.append(aux)
       i += 1

tri = Delaunay(points)

def find_neighbors(pindex, triang):

    return triang.vertex_neighbor_vertices[1][triang.vertex_neighbor_vertices[0][pindex]:triang.vertex_neighbor_vertices[0][pindex+1]]

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

new = ''

for p in range(len(points)):
    if printProgress:
        por = str(int((p / l) * 100))
        if (por != new):
            new = por
            print(new + "%")

    nrNeigh = 0
    for n in find_neighbors(p,tri):
        dist = distance(points[p][0],points[p][1],points[n][0],points[n][1])
        if (dist <= epsilon):
            nrNeigh += 1
            if plotNearestNeighbour:
                add_edge(p, n)
    if nrNeigh >= k:
        centerPointsPython.append(raw[p].tolist())
        center.append(p)
    else:
        candidates.append(p)
        candidatesPointsPython.append(raw[p].tolist())

# Move candidates from outlier to border
for cand in candidates:
    wasBorder = False
    for c in center:
        if distance(points[cand][0],points[cand][1],points[c][0], points[c][1]) <= epsilon:
            border.append(cand)
            borderPointsPython.append(raw[cand].tolist())
            wasBorder = True
            break
    if not wasBorder:
        outlier.append(cand)
        outlierPointsPython.append(raw[cand].tolist())

if plot:
    plotName = 'Technique:Delaunay '+'Data:' + file + ' | epsilon:' + str(epsilon) + ' | k:' + str(k)
    if save:
        plotName = 'TechniqueDelaunay '+'Data_' + str(len(points)) + '_epsilon:' + str(epsilon) + '_k:' + str(k)
        pp.saveWithEpsilonNeighbour('Delaunay',plotName, centerPointsPython, outlierPointsPython, borderPointsPython,
                                    neighbourEdge_points)
    elif plotNearestNeighbour:
        pp.plotWithEpsilonNeighbour(plotName, centerPointsPython, outlierPointsPython, borderPointsPython,
                                    neighbourEdge_points)
    else:
        pp.plot(plotName, centerPointsPython, outlierPointsPython, borderPointsPython)


