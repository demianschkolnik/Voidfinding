import numpy as np


file = 'Data/20irr2d_16384.dat'

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

print(points)

output = 'bio1'
file = open(output, 'w')

#c_ecolis(1, x, y, 0, {"pgalaxy"}, program p());

for p in points:
    file.write("c_ecolis(1," + str(p[0]) +"," + str(p[1]) + ", 0, {\"pgalaxy\"}, program p());\n")

file.close()