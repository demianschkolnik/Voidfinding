from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np


def run(file):
    f = open(file, 'r')
    i = 0
    first = 0
    for r in f:
        if first == 0:
            first += 1
        elif first == 1:
            l = int(r)
            first += 1
            raw = np.zeros((l, 3))
        else:
            row = r.split()
            raw[i, 0] = float(row[0])
            raw[i, 1] = float(row[1])
            raw[i, 2] = float(row[2])
            i += 1

    print(raw)

    fig = plt.figure()

    ax = fig.add_subplot(111, projection='3d')
    x = raw[:,0]
    y = raw[:,1]
    z = raw[:,2]

    ax.scatter(x, y, -z, zdir='z', c='black', depthshade=False, s=0.2, marker = ',')



    plt.show()


if __name__ == '__main__':

    run(file = 'Data/8sphere3d_r500_f500_4060.dat')