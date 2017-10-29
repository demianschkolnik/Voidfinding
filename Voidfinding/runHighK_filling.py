import kdTreeFunction as kdtf
import cropper
import filler

file = kdtf.kdTreeFinder(epsilon = 100, k=9, file='Data/20irr2d_2048.dat' )
cropped_file = file[:-4] + '_cropped.png'
cropper.crop(input_file=file, x=310, y=160, w=2205, h=1580, output_file=cropped_file)
filled_file = file[:-4] + '_filled.png'
filler.fill(img_file_input=cropped_file, img_file_output=filled_file, threshold=10000)