import random
import math


totalPoints = 10000
noisePoints = 25
radius = 200

file = open("NoiseSphere" + str(radius) + "R"+ str(totalPoints) + "P" + str(noisePoints) + "N.dat", "w")


file.write("2\n")

file.write(str(totalPoints+noisePoints)+"\n")

i = totalPoints

while i > 0:
    x = (random.random() * 2000) - 1000
    y = (random.random() * 2000) - 1000

    if math.sqrt(x*x+y*y)>radius:
        file.write(str(x)+" "+str(y)+"\n")
        i -= 1

i=noisePoints

while i>0:
    t = 2 * math.pi * random.random()
    u = random.random() + random.random()
    if u > 1:
        r = 2-u
    else:
        r = u

    r *= radius
    x = r * math.cos(t)
    y = r * math.sin(t)
    file.write(str(x) + " " + str(y) + "\n")
    i -= 1


file.close()