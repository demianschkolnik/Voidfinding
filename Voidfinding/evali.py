#!/bin/python2

import argparse
import pylab
import matplotlib
from random import choice
from shapely.geometry import Polygon
from shapely.geometry import MultiPolygon
from shapely.ops import cascaded_union

parser = argparse.ArgumentParser()
parser.add_argument('rootname', help='Root of the filenames to process')
parser.add_argument('-m', '--merge', help='Merge fragments (default: false)', action='store_true', default=False)
args = parser.parse_args()
root = args.rootname
merge = args.merge

plot1=[]
plot2=[]
orig=[]
group=[]

#Open file XXirr2d_YYYYY_real.dat with artificially generated voids
real = open('../realvoids/irregulars/'+root[:-4] + '_real.dat')

i = 0
for linr in real:
    #Line i: scale, x and y coordinates for i-th polygon
    vals = map(float,linr.split())
    sf = vals[0]
    cx = vals[1]
    cy = vals[2]
    #Open file irrvoid_<i>.dat
    svd = open('../realvoids/irregulars/voids/irrvoid_'+str(i)+'.dat')
    pol = []
    for linv in svd:
        #point * scale + center
        
        #Center coordinates
        point = map(float, linv.split())
        point[0]*=sf
        point[0]+=cx
        point[1]*=sf
        point[1]+=cy
        
        pol.append((point[0],point[1]))
    svd.close()
    orig.append(Polygon(pol))
    if merge:
        #Group for polygons whose nearest void is this one
        group.append([])
    else:
        group.append(None)
    i += 1
    #For final plot
    plot1.append(pol)
N = i
real.close()

#Read and process identified polygons
fnd = open('../results/data/irregulars/' + root + '.voids')
c=0
while True:
    try:
        #Read
        m = int(fnd.next())
        points = []
        for j in range(m):
            points.append(map(float, fnd.next().split()))
        pol = Polygon(points)
        #Add to nearest polygon group
        nearest = 0
        mindist = orig[0].centroid.distance(pol.centroid)
        for i in range(1,N):
            d = orig[i].centroid.distance(pol.centroid)
            if mindist > d:
                nearest = i
                mindist = d
        if merge:
            group[nearest].append(pol)
        elif group[nearest] is None or mindist < orig[nearest].centroid.distance(group[nearest].centroid):
            group[nearest] = pol
        c+=1
        #For final plot
        plot2.append(points)
    except StopIteration:
        break
fnd.close()

#Join polygons from each group and get recovery and error rates
rec_rates = []
err_rates = []
a1 = []
a2 = []
for i in range(N):
    if merge:
        #Union
        pol = cascaded_union(MultiPolygon(group[i]))
    else:
        #Standalone
        pol = group[i]
    if pol is None:
        a1.append(orig[i].area)
        a2.append(0)
        rec_rates.append(0)
        err_rates.append(1)
        continue
    #Intersect void with original polygon
    inter = pol.intersection(orig[i])
    #Unite void with original polygon
    union = pol.union(orig[i])
    #Get parameters
    a1.append(orig[i].area)
    a2.append(pol.area)
    rec_rates.append(inter.area / orig[i].area)
    if pol.area == 0.0:
        err_rates.append(1.0)
    else:
        err_rates.append(1.0 - inter.area / pol.area)
print " ".join("%.3f" % k for k in a1)
print " ".join("%.3f" % k for k in a2)
print " ".join("%.3f" % k for k in rec_rates)
print " ".join("%.3f" % k for k in err_rates)

################################
fig=pylab.figure()
ax = fig.add_subplot(111)
colores=['b','r','c','m','y']
xpoints=[]
ypoints=[]
i = 0
for void in plot1:
    c='b'
    poly = matplotlib.patches.Polygon(void, closed=True,fill=False,ec=c,lw=0.05)
    ax.add_patch(poly)
    ax.annotate(str(i),(orig[i].centroid.x,orig[i].centroid.y))
    i += 1
for void in plot2:
    c='r'
    poly = matplotlib.patches.Polygon(void, closed=True,fill=False,ec=c,lw=0.05)
    ax.add_patch(poly)

ax.scatter(xpoints,ypoints,c='k',s=0.15)
ax.set_xlabel('X',size='small')
ax.set_ylabel('Y',size='small')
ax.tick_params(axis='both', which='major', labelsize=8)
ax.tick_params(axis='both', which='minor', labelsize=8)
ax.set_aspect('equal')
ax.set_xlim(-1025,1025)
ax.set_ylim(-1025,1025)
pylab.savefig('../results/plots/irregulars/cmp'+root[:-4]+'.ps',bbox_layout='tight')

