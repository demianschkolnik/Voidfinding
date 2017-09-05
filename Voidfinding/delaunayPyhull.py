import numpy as np
from pyhull.delaunay import DelaunayTri
from pyhull.convex_hull import ConvexHull

manualEpsilon = False #Manual epsilon or calculated
epsilon    = 200 #epsilon is the distance to check for neighbours
k          = 12 #k is the number on the epsilon-neighborhood criterion
file       = 'Data/20irr2d_1024.dat' #File to be read


def distance(x1,y1,x2,y2):
   "distance between (x1,y1) and (x2,y2)"
   deltaXSquare = (x1-x2)**2
   deltaYSquare = (y1-y2)**2
   return (deltaXSquare+deltaYSquare) ** (0.5)

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
   else:
       row = r.split()
       aux = []
       aux.append((float)(row[0]))
       aux.append((float)(row[1]))
       points.append(aux)
       i += 1

delaunay = DelaunayTri(points)
hull = ConvexHull(points)
nrOfNeighbours  = [0] * l

edge_points = []
edges = set()

def add_edge(i, j):
    """Add a line between the i-th and j-th points, if not in the list already"""
    if (i, j) in edges or (j, i) in edges:
        # already added
        return
    edges.add((i, j))
    edge_points.append(points[[i, j]])


# loop over triangles:
# ia, ib, ic = indices of corner points of the triangle
for ia, ib, ic in delaunay.vertices:
    add_edge(ia, ib)
    add_edge(ib, ic)
    add_edge(ic, ia)

# add convex hull
for ia, ib in hull.vertices:
    add_edge(ia, ib)


print("")
