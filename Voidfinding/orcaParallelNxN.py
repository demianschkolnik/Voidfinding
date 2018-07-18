import numpy as np
from scipy.spatial import Delaunay
import plotPoints as pp
import time
import pyopencl as cl
from pyopencl import array
import openCLOrca as clo
import psutil
import os

def benchmarkMem(init):
    #MEMORY BENCHMARK
    process = psutil.Process(os.getpid())
    mem = process.memory_info().rss
    mem = mem >> 20
    print("mem:"+str(mem))

def run(epsilon, k, file, save, printProgress):
    # Manual epsilon or calculated
    # epsilon is the distance to check for neighbours
    # k is the number on the epsilon-neighborhood criterion
    # File to be read
    # Generation of neighbors on delaunay
    # save as image?
    # Print % of progress on console?

    plot = True  # Plot?
    plotNearestNeighbour = True  # Plot lines to epsilon-neighbours?

    removeOutliersFromGraph = True
    drawConvexHull = True

    def distance4(x1, y1, x2, y2):
        "distance between (x1,y1) and (x2,y2)"
        deltaXSquare = (x1 - x2) ** 2
        deltaYSquare = (y1 - y2) ** 2
        return (deltaXSquare + deltaYSquare) ** (0.5)

    def distance(a, b):
        "distance between point a and b"
        deltaXSquare = (a[0] - b[0]) ** 2
        deltaYSquare = (a[1] - b[1]) ** 2
        return (deltaXSquare + deltaYSquare) ** (0.5)

    void_triangles = []

    # Parse the read data
    lastTime = time.clock()
    print("Program Started "+str(time.clock()-start))
    print("Loading Data: ")

    f = open(file, 'r')
    i = 0
    first = 0
    points = []
    for r in f:
        if first == 0:
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

    # Create Delaunay Triangulation
    print("Data loaded: "+str(time.clock()-lastTime))
    print("Creating Delaunay Triangulation")
    lastTime = time.clock()

    tri = Delaunay(points)

    # Ids
    center = []
    outlier = []
    candidates = []
    border = []

    centerPointsPython = []
    outlierPointsPython = []
    candidatesPointsPython = []
    borderPointsPython = []

    neighbourEdge_points_center = []
    neighbour_edges_center = set()

    neighbourEdge_points_border = []
    neighbour_edges_border = set()

    def add_edge(i, j, neighbour_edges, neighbourEdge_points):
        """Add a line between the i-th and j-th points, if not in the list already"""
        if (i, j) in neighbour_edges or (j, i) in neighbour_edges:
            return
        neighbour_edges.add((i, j))
        neighbourEdge_points.append(raw[[i, j]])

    print("Finished Delaunay Triangulation: " + str(time.clock() - lastTime))

    print("Creating numpy arrays")
    lastTime = time.clock()

    lenP = len(points)
    vector = np.zeros((lenP, 1), cl.array.vec.float2)

    for p in range(len(points)):
        vector[p, 0] = (points[p][0], points[p][1])

    print("Finished numpy arrays: " + str(time.clock() - lastTime))
    print("Classifying points in GPU")
    lastTime = time.clock()

    result = clo.runParallelNxN(vector, k, epsilon, lenP)

    print("Finished Classifying points in GPU: " + str(time.clock() - lastTime))
    print("Processing data from parallel")
    lastTime = time.clock()

    #Process data from parallel:
    for r in range(len(result)):
        if result[r] == 0:
            outlierPointsPython.append(raw[r].tolist())
            outlier.append(r)
        elif result[r] == 1:
            centerPointsPython.append(raw[r].tolist())
            center.append(r)
        elif result[r] == 2:
            borderPointsPython.append(raw[r].tolist())
            border.append(r)

    p = 0
    new = 1

    # generate edges
    print("Finished processing data from parallel: " + str(time.clock() - lastTime))
    print("Adding Edges")
    lastTime = time.clock()

    for t in tri.simplices:
        if printProgress:
            por = str(int((p / len(tri.simplices)) * 100))
            if (por != new):
                new = por
                print(new + "%")
            p += 1

        edges_added = 0
        if t[0] < 0 or t[1] < 0 or t[2] < 0 or t[0] >= len(points) or t[1] >= len(points) or t[2] >= len(points):
            continue
        a, b, c = points[t[0]], points[t[1]], points[t[2]],

        if distance(a, b) <= epsilon and not (a in outlierPointsPython or b in outlierPointsPython):
            if a in borderPointsPython and b in borderPointsPython:
                add_edge(t[0], t[1], neighbour_edges_border, neighbourEdge_points_border)
            else:
                add_edge(t[0], t[1], neighbour_edges_center, neighbourEdge_points_center)
            edges_added += 1

        if distance(a, c) <= epsilon and not (a in outlierPointsPython or c in outlierPointsPython):
            if a in borderPointsPython and c in borderPointsPython:
                add_edge(t[0], t[2], neighbour_edges_border, neighbourEdge_points_border)
            else:
                add_edge(t[0], t[2], neighbour_edges_center, neighbourEdge_points_center)
            edges_added += 1
        if distance(b, c) <= epsilon and not (b in outlierPointsPython or c in outlierPointsPython):
            if b in borderPointsPython and c in borderPointsPython:
                add_edge(t[1], t[2], neighbour_edges_border, neighbourEdge_points_border)
            else:
                add_edge(t[1], t[2], neighbour_edges_center, neighbourEdge_points_center)
            edges_added += 1

        if (edges_added < 3):
            void_triangles.append((a, b, c))

    if drawConvexHull:
        for i in tri.convex_hull:
            add_edge(i[0], i[1], neighbour_edges_center, neighbourEdge_points_center)

    if removeOutliersFromGraph:
        outlierPointsPython = []

    benchmarkMem(initM)
    print("Finished Adding edges:" + str(time.clock() - lastTime))
    print("Finished!:"+str(time.clock()-start))

    if plot:
        plotName = 'Technique:Parallel ' + ') Data:' + file + ' | epsilon:' + str(
            epsilon) + ' | k:' + str(k)
        if save:
            plotName = 'TechniqueParallel ' + 'Data_' + str(len(points)) + '_epsilon:' + str(epsilon) + '_k:' + str(k)
            pp.saveWithEpsilonNeighbourBig('Delaunay', plotName, centerPointsPython, outlierPointsPython,
                                           borderPointsPython,
                                           neighbourEdge_points_center)
        elif plotNearestNeighbour:
            pp.plotWithEpsilonNeighbour2Edges(plotName, centerPointsPython, outlierPointsPython, borderPointsPython,
                                              neighbourEdge_points_center, neighbourEdge_points_border, void_triangles,
                                              color1='black', color2='black', color3='black',
                                              color4='none', color5='none')
        else:
            pp.plot(plotName, centerPointsPython, outlierPointsPython, borderPointsPython)


if __name__ == '__main__':
    start = time.clock()
    #define initial used memory in mb
    mem = psutil.virtual_memory()
    initM = mem.used >> 20
    run(
        epsilon=70,
        k=19,
        file='Data/20irr2d_262144.dat',
        save=False,
        printProgress=False
    )