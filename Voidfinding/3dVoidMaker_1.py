import math

def distance(x, y):
    return  math.sqrt(sum([(a - b) ** 2 for a, b in zip(x, y)]))

def isInSphere(point, voidCenters, radius):
    for voidCenter in voidCenters:
        if distance(voidCenter,point) < radius:
            return False
    return True

def run(file, focus, radius):

    voidCenters = []
    for i in [-1,1]:
        for j in [-1,1]:
            for k in [-1,1]:
                a = focus*i
                b = focus*j
                c = focus*k
                voidCenters.append([a,b,c])

    print(voidCenters)
    f = open(file, 'r')
    first = 0
    points = []
    for r in f:
        if first == 0:
            first = 1
        elif first == 1:
            first += 1
        else:
            row = r.split()
            aux = []
            aux.append((float)(row[0]))
            aux.append((float)(row[1]))
            aux.append((float)(row[2]))
            if isInSphere(aux, voidCenters, radius):
                points.append(aux)

    print(len(points))

    #writing file
    wName = "Data/8sphere3d_r"+  str(radius) + "_f" + str(focus) + "_" + str(len(points)) + ".dat"
    fileW = open(wName, "w")
    fileW.write("3\n")
    fileW.write(str(len(points))+"\n")
    for tri in points:
        fileW.write(str(tri[0]) + "\t" + str(tri[1]) + "\t" + str(tri[2]) + "\n")

    fileW.close()


if __name__ == '__main__':

    run(file = 'Data/noVoids_3d_8192.dat',
        focus = 500,
        radius = 500)