import cv2
import numpy as np
from random import randint


img_file = 'Figures/croppedIMG.png'
img = cv2.imread(img_file, cv2.IMREAD_COLOR)           # rgb
alpha_img = cv2.imread(img_file, cv2.IMREAD_UNCHANGED) # rgba
gray_img = cv2.imread(img_file, cv2.IMREAD_GRAYSCALE)  # grayscale

print(type(img))
print('RGB shape: ', img.shape)     # Rows, cols, channels
print('ARGB shape:', alpha_img.shape)
print('Gray shape:', gray_img.shape)
print('img.dtype: ', img.dtype)
print('img.size: ', img.size)

def colorize(img, i, j):
    if i<0 or j<0 or i>=img.shape[0] or j>=img.shape[1]:
        return
    if img[i,j][0] != 255 and img[i,j][1] != 255 and img[i,j][2] != 255:
        return
    r = randint(0, 255)
    g = randint(0, 255)
    b = randint(0, 255)
    seedPoint = (i, j)
    h, w = img.shape[:2]
    mask = np.zeros((h + 2, w + 2), np.uint8)
    try:
        cv2.floodFill(image=img, mask=mask, seedPoint=seedPoint, newVal=(r,g,b))
    except:
        return


for i in range(0,img.shape[1]):
    for j in range(0,img.shape[0]):
        print(i,j)
        colorize(img,i,j)

cv2.imwrite("Figures/ChangingTest2.png", img)