import numpy as np
from scipy.spatial import Delaunay
import plotPoints as pp
import time
#import psutil
#import os

#def benchmarkMem(init):
    #MEMORY BENCHMARK
    #process = psutil.Process(os.getpid())
    #mem = process.memory_info().rss
    #mem = mem >> 20
    #print("mem:"+str(mem))

def run(epsilon, k, file, gen, save, printProgress):
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

    # Parse de read data
    print("Loading Data"+str(time.clock()-start))


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
    print("Create Delaunay Triangulation"+str(time.clock()-start))

    tri = Delaunay(points)

    def find_neighbors(pindex, triang):
        return triang.vertex_neighbor_vertices[1][
               triang.vertex_neighbor_vertices[0][pindex]:triang.vertex_neighbor_vertices[0][pindex + 1]]

    def find_neighborsFromList(pindexList, triang):
        output = []
        for pindex in pindexList:
            neighbors = find_neighbors(pindex, triang)
            output = output + neighbors.tolist()
        return list(set(output))

    def find_neighborsGen(pindex, triang, gen):
        neighbors = find_neighbors(pindex, triang)
        for i in range(0, gen - 1):
            neighbors = find_neighborsFromList(neighbors, triang)
        return neighbors

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

    new = ''

    print("Classifying points"+str(time.clock()-start))

    for p in range(len(points)):
        if printProgress:
            por = str(int((p / l) * 100))
            if (por != new):
                new = por
                print(new + "%")

        nrNeigh = 0
        for n in find_neighborsGen(p, tri, gen):
            dist = distance4(points[p][0], points[p][1], points[n][0], points[n][1])
            if (dist <= epsilon):
                nrNeigh += 1
                # if plotNearestNeighbour:
                # add_edge(p, n)
                if nrNeigh>=k:
                    break
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
            if distance4(points[cand][0], points[cand][1], points[c][0], points[c][1]) <= epsilon:
                border.append(cand)
                borderPointsPython.append(raw[cand].tolist())
                wasBorder = True
                break
        if not wasBorder:
            outlier.append(cand)
            outlierPointsPython.append(raw[cand].tolist())

    p = 0
    new = 1

    # generate edges
    print("Adding Edges"+str(time.clock()-start))

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

    #benchmarkMem(initM)
    print("Finished!:"+str(time.clock()-start))

    if plot:
        plotName = 'Technique:Delaunay ' + ' gen(' + str(gen) + ') Data:' + file + ' | epsilon:' + str(
            epsilon) + ' | k:' + str(k)
        if save:
            plotName = 'TechniqueDelaunay ' + 'Data_' + str(len(points)) + '_epsilon:' + str(epsilon) + '_k:' + str(k)
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
    #mem = psutil.virtual_memory()
    #initM = mem.used >> 20
    run(
        epsilon=1000,
        k=1,
        file='Data/30sphere2d_100000.dat',
        gen=4,
        save=False,
        printProgress=True
    )

    # run(
    #     epsilon=70,
    #     k=14,
    #     file='Data/30sphere2d_100000.dat',
    #     gen=4,
    #     save=False,
    #     printProgress=False
    # )