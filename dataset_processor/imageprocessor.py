
from __future__ import print_function
from PIL import Image
import os, sys

# Resize all the images in the data folder and put them in a new sub-directory
def batch_resize(folders, w, h):
    for folder in folders:
        path = 'data/' + folder + '/'
        dirs = os.listdir( path )
        resized_img_path = 'data/' + folder + '_resized/'
        if not os.path.exists(resized_img_path):
            os.makedirs(resized_img_path)
        for item in dirs:
            if os.path.isfile(path + item):
                im = Image.open(path + item)
                imResize = im.resize((w,h), Image.ANTIALIAS)
                filename = os.path.basename(path + item)
                filename, extension = os.path.splitext(filename)
                imResize.save(resized_img_path + filename + '_resized.png', 'png')

# creates a file with all the pixels of each image written out with ' ' delimiter
# images parameter is an array of PIL Images
def createDS(images):
    f = open('shapes_data.txt', 'w+')
    f.truncate()
    for image in images:
        pixels = list(image[1].getdata())
        pixels_string = ' '.join(map(str, pixels))
        classification = getShape(image[0])
        print(pixels_string + classification, file = f)

# make a PIL Image instance for each image and return a list of images
def createImages(folders):
    images = []
    for folder in folders:
        path = 'data/' + folder + '_resized/'
        if os.path.exists(path):
            for item in os.listdir(path):
                new_image = Image.open(path + item)
                new_image = new_image.convert('L')
                images = images + [(folder, new_image)]
    return images

# returns an integer value associated with a shape in a given folder to append to the end of each data row
def getShape(folder):
    # triangles are classification 1
    if (folder == 'triangle'):
        return ' 1'
    # squares are classification 2
    elif(folder == 'square'):
        return ' 2'
    # circles are classification 3
    elif (folder == 'circle'):
        return ' 3'

# create a list of file names where the images are stored
folders = ['triangle', 'circle', 'square']

batch_resize(folders, 500, 500)
createDS(createImages(folders))
