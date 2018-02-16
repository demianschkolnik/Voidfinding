import time
import runHighK_filling
import scipyDelaunayGen2

if __name__ == '__main__':

    #options:
    # 1: KDTree with High k + filling
    # 2: Delaunay with more generations and removing edges, classifying triangles
    option = 1
    files = ['20irr2d_1024.dat','20irr2d_2048.dat','20irr2d_4096.dat','20irr2d_8192.dat','20irr2d_16384.dat',
             '20irr2d_32768.dat','20irr2d_65536.dat','20irr2d_131072.dat','20irr2d_262144.dat']
    output = open('results.txt', 'w')
    epsilon = 100
    k = 20
    #just for option 2:
    gen = 3

    for file in files:
        start_time = time.time()
        fileName = 'Data/' + file
        print(fileName + ":")
        if option == 1:
            runHighK_filling.run(fileName,epsilon = 100, k = 10)
        elif option == 2:
            scipyDelaunayGen2.run(epsilon, k, fileName, gen, save=True, printProgress = False)
        runTime = round(time.time() - start_time, 2)
        output.write( file + ":" + str(runTime) + "\n")
    output.close()