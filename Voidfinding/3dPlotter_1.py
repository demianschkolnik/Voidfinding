from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation


def runTest1():
    from mpl_toolkits.mplot3d import axes3d
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # load some test data for demonstration and plot a wireframe
    X, Y, Z = axes3d.get_test_data(0.1)
    ax.plot_wireframe(X, Y, Z, rstride=5, cstride=5)

    # rotate the axes and update
    for angle in range(0, 3600):
        ax.view_init(30, angle)
        plt.draw()
        plt.pause(.001)

def run4():
    from mpl_toolkits.mplot3d import Axes3D
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection
    import matplotlib.pyplot as plt

    fig = plt.figure()
    ax = Axes3D(fig)
    x = [0, 1, 1]
    y = [0, 0, 1]
    z = [0, 1, 0]
    verts = [list(zip(x, y, z))]
    verts2 = [(0,0,0),(-1,0,-1),(-1,-1,0)]
    verts.append(verts2)
    print(verts)
    ax.add_collection3d(Poly3DCollection(verts), zs='z')
    plt.show()

def run3():
    raw = np.random.rand(100,3)
    fig = plt.figure()

    ax = fig.add_subplot(111, projection='3d')
    x = raw[:, 0]
    y = raw[:, 1]
    z = raw[:, 2]

    ax.scatter(x, y, -z, zdir='z', c='black', depthshade=False, s=1, marker='.')

    def rotate(angle):
        ax.view_init(azim=angle)

    print("Making animation")
    rot_animation = animation.FuncAnimation(fig, rotate, frames=np.arange(0, 362, 2), interval=100)
    rot_animation.save('rotation.gif', dpi=80, writer='imagemagick')

def run(file):
    print("Opening file")
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

    print("file opened. Plotting.")
    fig = plt.figure()

    ax = fig.add_subplot(111, projection='3d')
    x = raw[:,0]
    y = raw[:,1]
    z = raw[:,2]

    ax.scatter(x, y, -z, zdir='z', c='black', depthshade=False, s=1, marker = '.')

    #plt.show()
    def rotate(angle):
        ax.view_init(azim=angle)

    print("Making animation")
    rot_animation = animation.FuncAnimation(fig, rotate, frames=np.arange(0, 362, 2), interval=100)
    print("Saving animation")
    rot_animation.save('rotation1.gif', dpi=80, writer='imagemagick')
    print("done!")


if __name__ == '__main__':

    run(file = 'Data/regular_10_noVoids_68921.dat')
