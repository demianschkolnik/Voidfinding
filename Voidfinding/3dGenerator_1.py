import random

def run2():
    count = 0
    for x in range(-1000,1001,50):
        for y in range(-1000, 1001,50):
            for z in range(-1000, 1001,50):
                count +=1
    wName = "Data/regular_10_noVoids_" + str(count) + ".dat"
    fileW = open(wName, "w")
    fileW.write("3\n")
    fileW.write(str(count) + "\n")
    for x in range(-1000,1001,50):
        for y in range(-1000, 1001,50):
            for z in range(-1000, 1001,50):
                fileW.write(str(x) + "\t" + str(y) + "\t" + str(z) + "\n")



def run(file):
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
            #generate 3rd random point
            r = random.uniform(-1000,1000)
            aux.append(r)

            points.append(aux)

    print(len(points))
    print(points)

    #writing file
    wName = "Data/noVoids_3d_" + str(len(points)) + ".dat"
    fileW = open(wName, "w")
    fileW.write("3\n")
    fileW.write(str(len(points))+"\n")
    for tri in points:
        fileW.write(str(tri[0]) + "\t" + str(tri[1]) + "\t" + str(tri[2]) + "\n")

    fileW.close()

if __name__ == '__main__':

    #run(file = 'Data/20irr2d_8192.dat')
    run2()