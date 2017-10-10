from scipy import spatial
import numpy as np
import plotPoints as pp

manualEpsilon = False #Manual epsilon or calculated
epsilon    = 70 #epsilon is the distance to check for neighbours
k          = 9 #k is the number on the epsilon-neighborhood criterion
file       = 'Data/20irr2d_2048.dat' #File to be read
plot = True #Plot?
plotNearestNeighbour = False #Plot lines to epsilon-neighbours?
printProgress = True #Print % of progress on console?
justPlotBorder = False
justPlotCenter = False


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
       raw = np.zeros((l,2))
   else:
       row = r.split()
       aux = []
       raw[i,0] = float(row[0])
       raw[i,1] = float(row[1])
       aux.append(float(row[0]))
       aux.append(float(row[1]))
       points.append(aux)
       i += 1

def distance(x1,y1,x2,y2):
   "distance between (x1,y1) and (x2,y2)"
   deltaXSquare = (x1-x2)**2
   deltaYSquare = (y1-y2)**2
   return (deltaXSquare+deltaYSquare) ** (0.5)

tree = spatial.KDTree(points)

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

def add_edge(i, j, data):
    """Add a line between the i-th and j-th points, if not in the list already"""
    if (i, j) in neighbour_edges or (j, i) in neighbour_edges:
        return
    neighbour_edges.add((i, j))
    neighbourEdge_points.append(data[ [i, j] ])

new = ''
#check for center objects.
for i in range(0,l):
   if printProgress:
       por =  str(int((i/l)*100))
       if(por != new):
           new = por
           print(new+"%")

   epsNeighbors = tree.query_ball_point(points[i],epsilon)

   wasCenter = False
   if len(epsNeighbors) >= (k+1): #kd tree counts itself!
       centerPointsPython.append(raw[i].tolist())
       center.append(i)
       wasCenter = True
   else:
       candidates.append(i)
       candidatesPointsPython.append(raw[i].tolist())

   if justPlotBorder:
       if plotNearestNeighbour:
           for ne in epsNeighbors:
               if i != ne and not wasCenter:
                   add_edge(i, ne, raw)
   elif not justPlotCenter:
       if plotNearestNeighbour:
           for ne in epsNeighbors:
               if i != ne:
                   add_edge(i, ne, raw)

#plot just centers
if justPlotCenter:
    tree2 = spatial.KDTree(centerPointsPython)
    for j in range(0,len(centerPointsPython)):
        if printProgress:
            por = str(int((j / len(centerPointsPython)) * 100))
            if (por != new):
                new = por
                print(new + "%")

        epsNeighbors2 = tree2.query_ball_point(centerPointsPython[j],epsilon)
        for ne in epsNeighbors2:
            if j != ne:
                add_edge(j, ne, np.array(centerPointsPython))

#Move candidates from outlier to border
for cand in candidates:
   wasBorder = False
   for c in center:
       if distance(points[cand][0],points[cand][1],points[c][0],points[c][1]) <= epsilon:
           border.append(cand)
           borderPointsPython.append(raw[cand].tolist())
           wasBorder = True
           break
   if not wasBorder:
       outlier.append(cand)
       outlierPointsPython.append(raw[cand].tolist())

#TEST
if justPlotBorder:
    centerPointsPython = []
    outlierPointsPython = []
elif justPlotCenter:
    outlierPointsPython = []
    borderPointsPython = []

if plot:
    plotName = 'Technique:KDTree '+'Data:' + file + ' | epsilon:' + str(epsilon) + ' | k:' + str(k)
    if plotNearestNeighbour:
        pp.plotWithEpsilonNeighbour(plotName, centerPointsPython, outlierPointsPython, borderPointsPython,neighbourEdge_points)
    else:
        pp.plot(plotName, centerPointsPython, outlierPointsPython, borderPointsPython)
