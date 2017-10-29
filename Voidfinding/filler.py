import cv2
from random import randint

def fill(img_file_input, img_file_output, threshold=10000):
    print('Filling:' + img_file_input)
    img = cv2.imread(img_file_input, cv2.IMREAD_COLOR)           # rgb

    # alpha_img = cv2.imread(img_file, cv2.IMREAD_UNCHANGED) # rgba
    # gray_img = cv2.imread(img_file, cv2.IMREAD_GRAYSCALE)  # grayscale

    # print(type(img))
    # print('RGB shape: ', img.shape)     # Rows, cols, channels
    # print('ARGB shape:', alpha_img.shape)
    # print('Gray shape:', gray_img.shape)
    # print('img.dtype: ', img.dtype)
    # print('img.size: ', img.size)

    def isWhite(color):
        return color[0] == 255 and color[1] == 255 and color[2] == 255

    def paint(img,points,color):
        for p in points:
            img[p] = color

    def colorize(img, i, j):
        if i<0 or j<0 or i>=img.shape[0] or j>=img.shape[1]:
            return
        if not isWhite(img[i,j]):
            return
        toCheck = []
        voidPoints = []
        toCheck.append((i,j))
        r = randint(0, 255)
        g = randint(0, 255)
        b = randint(0, 255)
        while len(toCheck) > 0:
            p = toCheck.pop()
            voidPoints.append(p)
            img[p[0], p[1]] = (0, 0, 0)
            if (p[0] + 1 < img.shape[0]) and (isWhite(img[p[0]+1,p[1]])):
                toCheck.append((p[0]+1,p[1]))
            if (p[0] - 1 >= 0) and (isWhite(img[p[0] - 1, p[1]])):
                toCheck.append((p[0]-1,p[1]))
            if (p[1] + 1 < img.shape[1]-1) and (isWhite(img[p[0], p[1] +1])):
                toCheck.append((p[0],p[1]+1))
            if (p[1] - 1 >= 0) and (isWhite(img[p[0], p[1] - 1])):
                toCheck.append((p[0],p[1]-1))
        if len(voidPoints) >= threshold:
            paint(img,voidPoints,(r,g,b))

    new = 1
    for i in range(0,img.shape[0]):
        por = str(int((i / img.shape[0]) * 100))
        if (por != new):
            new = por
            print(new + "%")
        for j in range(0,img.shape[1]):
            colorize(img,i,j)

    cv2.imwrite(img_file_output, img)