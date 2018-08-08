from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
jet = plt.get_cmap('jet')
from matplotlib import animation
from mpl_toolkits.mplot3d.art3d import Poly3DCollection



def plot(name, centerPointsPython, outlierPointsPython, borderPointsPython):
    centerPointsNP = np.array(centerPointsPython)
    outlierPointsNP = np.array(outlierPointsPython)
    borderPointsNP = np.array(borderPointsPython)

    plt.figure()
    plt.title(name)
    plt.plot(borderPointsNP[:, 0], borderPointsNP[:, 1], 'ko', markersize=1, color='blue', label="Border Points")
    plt.plot(centerPointsNP[:, 0], centerPointsNP[:, 1], 'ko', markersize=1, color='cyan', label="Center Points")
    plt.plot(outlierPointsNP[:, 0], outlierPointsNP[:, 1], 'ko', markersize=1, color='green', label="Outlier Points")

    plt.legend(loc=4, fontsize='small')

    plt.xlim(-1050, 1050)
    plt.ylim(-1050, 1050)

    plt.show()

def plotWithEpsilonNeighbour(name, centerPointsPython, outlierPointsPython, borderPointsPython, edge_points):
    centerPointsNP = np.array(centerPointsPython)
    outlierPointsNP = np.array(outlierPointsPython)
    borderPointsNP = np.array(borderPointsPython)

    plt.figure()
    plt.title(name)
    if len(borderPointsNP) > 0:
        plt.plot(borderPointsNP[:, 0], borderPointsNP[:, 1], 'ko', markersize=1.2, color='blue', label="Border Points")
    if len(centerPointsNP) > 0:
        plt.plot(centerPointsNP[:, 0], centerPointsNP[:, 1], 'ko', markersize=1.2, color='cyan', label="Center Points")
    if len(outlierPointsNP) > 0:
        plt.plot(outlierPointsNP[:, 0], outlierPointsNP[:, 1], 'ko', markersize=1.2, color='green',
                 label="Outlier Points")

    lines = LineCollection(edge_points, color='black', linewidths=0.2)
    plt.gca().add_collection(lines)

    # x1 = [-100, 120]
    # y1 = [100, 400]
    # plt.plot(x1, y1, marker='None', lw=1)

    plt.legend(loc=4, fontsize='small')

    plt.xlim(-1050, 1050)
    plt.ylim(-1050, 1050)

    plt.show()

def plotWithEpsilonNeighbour2Edges(name, centerPointsPython, outlierPointsPython, borderPointsPython, edge_points1,
                                   edge_points2, polygons,
                                   color1='blue', color2='cyan', color3='green', color4='black', color5='red'):
    centerPointsNP = np.array(centerPointsPython)
    outlierPointsNP = np.array(outlierPointsPython)
    borderPointsNP = np.array(borderPointsPython)

    plt.figure()
    plt.title(name)
    if len(borderPointsNP) > 0 and color1!='none':
        plt.plot(borderPointsNP[:, 0], borderPointsNP[:, 1], '.', markersize=0.5, color=color1)
    if len(centerPointsNP) > 0 and color2!='none':
        plt.plot(centerPointsNP[:, 0], centerPointsNP[:, 1], '.', markersize=0.5, color=color2)
    if len(outlierPointsNP) > 0 and color3!='none':
        plt.plot(outlierPointsNP[:, 0], outlierPointsNP[:, 1], '.', markersize=0.5, color=color3)

    if color4!='none':
        lines = LineCollection(edge_points1, color=color4, linewidths=0.2)
        plt.gca().add_collection(lines)

    if color5 != 'none':
        lines2 = LineCollection(edge_points2, color=color5, linewidths=0.5)
        plt.gca().add_collection(lines2)

    patches = []
    for p in polygons:
        polygon = Polygon(p, True)
        patches.append(polygon)

    p = PatchCollection(patches, alpha=0.4)
    plt.gca().add_collection(p)

    # x1 = [-100, 120]
    # y1 = [100, 400]
    # plt.plot(x1, y1, marker='None', lw=1)

    plt.legend(loc=4, fontsize='small')

    plt.xlim(-1050, 1050)
    plt.ylim(-1050, 1050)

    plt.show()

def plotWithEpsilonNeighbourSingle(name, points, edges):
    pointsNP = np.array(points)

    plt.figure()
    plt.title(name)
    if len(pointsNP) > 0:
        plt.plot(pointsNP[:, 0], pointsNP[:, 1], 'ko', markersize=1.0, color='blue', label="Points")

    lines = LineCollection(edges, color='black', linewidths=0.2)
    plt.gca().add_collection(lines)

    # x1 = [-100, 120]
    # y1 = [100, 400]
    # plt.plot(x1, y1, marker='None', lw=1)

    plt.legend(loc=4, fontsize='small')

    plt.xlim(-1050, 1050)
    plt.ylim(-1050, 1050)

    plt.show()

def saveWithEpsilonNeighbourBig(folderName, name, centerPointsPython, outlierPointsPython, borderPointsPython, edge_points):
    centerPointsNP = np.array(centerPointsPython)
    outlierPointsNP = np.array(outlierPointsPython)
    borderPointsNP = np.array(borderPointsPython)

    plt.figure()
    plt.title(name)
    if len(borderPointsNP) > 0:
        plt.plot(borderPointsNP[:, 0], borderPointsNP[:, 1], 'ko', markersize=1.2, color='blue', label="Border Points")
    if len(centerPointsNP) > 0:
        plt.plot(centerPointsNP[:, 0], centerPointsNP[:, 1], 'ko', markersize=1.2, color='cyan', label="Center Points")
    if len(outlierPointsNP) > 0:
        plt.plot(outlierPointsNP[:, 0], outlierPointsNP[:, 1], 'ko', markersize=1.2, color='green',
                 label="Outlier Points")

    lines = LineCollection(edge_points, color='black', linewidths=0.2)
    plt.gca().add_collection(lines)

    # x1 = [-100, 120]
    # y1 = [100, 400]
    # plt.plot(x1, y1, marker='None', lw=1)

    plt.legend(loc=4, fontsize='small')

    plt.xlim(-1050, 1050)
    plt.ylim(-1050, 1050)

    saveFile = 'Figures/' + folderName + '/' + name +'.png'
    plt.savefig(saveFile, bbox_inches='tight', dpi=400 )

def saveWithEpsilonNeighbour(folderName, name, points, edges):
    pointsNP = np.array(points)

    plt.figure()
    plt.title(name)
    if len(pointsNP) > 0:
        plt.plot(pointsNP[:, 0], pointsNP[:, 1], 'ko', markersize=1.0, color='blue', label="Points")


    lines = LineCollection(edges, color='black', linewidths=0.2)
    plt.gca().add_collection(lines)

    # x1 = [-100, 120]
    # y1 = [100, 400]
    # plt.plot(x1, y1, marker='None', lw=1)

    plt.legend(loc=4, fontsize='small')

    plt.xlim(-1050, 1050)
    plt.ylim(-1050, 1050)

    saveFile = 'Figures/' + folderName + '/' + name + '.png'
    plt.savefig(saveFile, bbox_inches='tight', dpi=400)

def saveWithEpsilonNeighbourNoLabels(folderName, name, points, edges):
    pointsNP = np.array(points)

    plt.figure()
    plt.title(name)
    if len(pointsNP) > 0:
        plt.plot(pointsNP[:, 0], pointsNP[:, 1], 'ko', markersize=1.0, color='blue')


    lines = LineCollection(edges, color='black', linewidths=0.2)
    plt.gca().add_collection(lines)

    # x1 = [-100, 120]
    # y1 = [100, 400]
    # plt.plot(x1, y1, marker='None', lw=1)

    plt.legend(loc=4, fontsize='small')

    plt.xlim(-1050, 1050)
    plt.ylim(-1050, 1050)

    saveFile = 'Figures/' + folderName + '/' + name + '.png'
    plt.savefig(saveFile, bbox_inches='tight', dpi=400)

def plot3d(name, centerPointsPython, borderPointsPython, outlierPointsPython, voidTriangles):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    if centerPointsPython:
        centerPoints = np.array(centerPointsPython)
        x, y, z = centerPoints[:, 0], centerPoints[:, 1], centerPoints[:, 2]
        ax.scatter(x, y, -z, zdir='z', c='black', depthshade=False, s=1, marker='.')
    if borderPointsPython:
        borderPoints = np.array(borderPointsPython)
        x, y, z = borderPoints[:, 0], borderPoints[:, 1], borderPoints[:, 2]
        ax.scatter(x, y, -z, zdir='z', c='blue', depthshade=False, s=1, marker='.')
    if outlierPointsPython:
        outlierPoints = np.array(outlierPointsPython)
        x, y, z = outlierPoints[:, 0], outlierPoints[:, 1], outlierPoints[:, 2]
        ax.scatter(x, y, -z, zdir='z', c='red', depthshade=False, s=1, marker='.')

    cleanedTriangles = []
    limit = 900
    for t in voidTriangles:
        isborder = False
        for p in t:
            if abs(p[0])>limit or abs(p[1])>limit or abs(p[2])>limit:
                isborder = True
        if not isborder:
            cleanedTriangles.append(t)

    ax.add_collection3d(Poly3DCollection(cleanedTriangles, alpha=0.2), zs='z')

    #plt.show()

    def rotate(angle):
        ax.view_init(azim=angle)

    print("Making animation")
    rot_animation = animation.FuncAnimation(fig, rotate, frames=np.arange(0, 362, 2), interval=100)
    rot_animation.save('rotation2.gif', dpi=80, writer='imagemagick')

