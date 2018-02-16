import cv2

def crop(input_file, x, y, w, h, output_file, printProgress):
    if printProgress:
        print('Cropping:' + input_file)
    img = cv2.imread(input_file)
    crop_img = img[y:h, x:w] # Crop from x, y, w, h -> 100, 200, 300, 400
    # NOTE: its img[y: y + h, x: x + w] and *not* img[x: x + w, y: y + h]
    cv2.imwrite(output_file, crop_img)