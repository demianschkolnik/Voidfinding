import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection


def plot(name, centerPointsPython, outlierPointsPython, borderPointsPython):
    centerPointsNP = np.array(centerPointsPython)
    outlierPointsNP = np.array(outlierPointsPython)
    borderPointsNP = np.array(borderPointsPython)

    plt.figure()
    plt.title(name)
    plt.plot(borderPointsNP[:, 0], borderPointsNP[:, 1], 'ko', markersize=1.2, color='blue', label="Border Points")
    plt.plot(centerPointsNP[:, 0], centerPointsNP[:, 1], 'ko', markersize=1.2, color='cyan', label="Center Points")
    plt.plot(outlierPointsNP[:, 0], outlierPointsNP[:, 1], 'ko', markersize=1.2, color='green', label="Outlier Points")

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

def saveWithEpsilonNeighbour(name, centerPointsPython, outlierPointsPython, borderPointsPython, edge_points):
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

    saveFile = 'Figures/figure' + name +'.png'
    plt.savefig(saveFile, bbox_inches='tight')