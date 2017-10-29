import numpy as np
from scipy.spatial import Delaunay
import plotPoints as pp

manualEpsilon = False #Manual epsilon or calculated
epsilon    = 60 #epsilon is the distance to check for neighbours
file       = 'Data/20irr2d_8192.dat' #File to be read

plot = True #Plot?
plotNearestNeighbour = True #Plot lines to epsilon-neighbours?
save = False #save as image?
printProgress = True #Print % of progress on console?
drawConvexHull = True

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

neighbourEdge_points = []
neighbour_edges = set()

def add_edge(i, j, neighbour_edges,neighbourEdge_points):
    """Add a line between the i-th and j-th points, if not in the list already"""
    if (i, j) in neighbour_edges or (j, i) in neighbour_edges:
        return
    neighbour_edges.add((i, j))
    neighbourEdge_points.append(raw[ [i, j] ])

new = ''

p = 0
new = 1

#generate edges
print("Adding Edges")
for t in tri.simplices:
    if printProgress:
        por = str(int((p / len(tri.simplices)) * 100))
        if (por != new):
            new = por
            print(new + "%")
        p += 1
    p1,p2,p3 = t
    if distance(points[p1][0],points[p1][1],points[p2][0],points[p2][1]) <= epsilon:
        add_edge(p1,p2,neighbour_edges,neighbourEdge_points)
    if distance(points[p1][0],points[p1][1],points[p3][0],points[p3][1]) <= epsilon:
        add_edge(p1,p3,neighbour_edges,neighbourEdge_points)
    if distance(points[p2][0],points[p2][1],points[p3][0],points[p3][1]) <= epsilon:
        add_edge(p2,p3,neighbour_edges,neighbourEdge_points)

if drawConvexHull:
    for i in tri.convex_hull:
        add_edge(i[0],i[1],neighbour_edges,neighbourEdge_points)


if plot:
    plotName = 'Technique:Delaunay ' + ') Data:' + file + ' | epsilon:' + str(epsilon)
    if save:
        plotName = 'TechniqueDelaunay '+'Data_' + str(len(points)) + '_epsilon:' + str(epsilon)
        pp.saveWithEpsilonNeighbour('Delaunay',plotName, points, neighbourEdge_points)
    else:
        pp.plotWithEpsilonNeighbourSingle(plotName, points, neighbourEdge_points)



