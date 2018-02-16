import kdTreeFunction as kdtf
import cropper
import filler

def run(filename,epsilon,k, printProgress = False):
    print("Building KDTree")
    file = kdtf.kdTreeFinder(epsilon, k, filename, printProgress)

    print("Cropping")
    cropped_file = file[:-4] + '_cropped.png'
    cropper.crop(input_file=file, x=310, y=160, w=2205, h=1580, output_file=cropped_file, printProgress = printProgress)

    print("Filling")
    filled_file = file[:-4] + '_filled.png'
    filler.fill(img_file_input=cropped_file, img_file_output=filled_file, threshold=10000, printProgress = printProgress)

if __name__ == '__main__':
    run(filename='Data/20irr2d_8192.dat',epsilon = 100, k = 10, printProgress=True)


