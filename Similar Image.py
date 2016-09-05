from urllib import request
from urllib.error import URLError
from PIL import Image
from sys import argv
import os
import glob
import imghdr

#FUNCTIONS
def getPixels(image):
    "Returns the pixels in the given image"
    pixels = []
    for i in range(3):
        for j in range(3):
            xy = i, j
            pixels.append(image.getpixel(xy))
    return pixels

def getPixelsFromFile(fileContents):
    old_index_of_comma = 0;
    pixels = []
    fileContents = str(fileContents)
    while(True):
        try:
            index_of_comma = fileContents.index(",", (old_index_of_comma + 1)) 
            pixels.append(fileContents[old_index_of_comma + 2:index_of_comma].split())
            old_index_of_comma = index_of_comma
        except ValueError:
            break
    return pixels
 
def writeImageData(image):
    data = ""
    pixels = getPixels(image)
    
    for pixelData in pixels:
        data += str(pixelData[0]) + " " + str(pixelData[2]) + " " + str(pixelData[2]) + ", "
    return data

#Assign command line arguments
if len(argv) is not 2 and argv[0] is not "":
    print("Usage: file path or url to image")
    quit()
else:
    image_path = argv[1]

#Set up folders and pathnames for where to save the scaled images
path_of_script = os.path.dirname(os.path.realpath(argv[0]))
folder_name = "/Scaled Images/"
#check if the folder exists
if not os.path.exists(path_of_script + folder_name):
    os.makedirs(path_of_script + folder_name)


#Go through the pictures directoy and create 3 by 3 representations of images
for image in glob.glob(os.getenv("HOME") + "/Pictures/*"):
    image_type = imghdr.what(image)

    #If the image is valid, add its 3 by 3 representation to the directory
    if image_type is "jpeg" or "bmp" or "png" or "tiff":
        file,ext = os.path.splitext(image)
        if "_scaled" not in file:
            img = Image.open(image)
            size = 3, 3
            img = img.resize(size, Image.NEAREST)

            #Save the image to the same folder this script is in
            index_of_last_slash = file.rindex("/")
            picture_name = file[index_of_last_slash + 1:]

            with open(path_of_script + folder_name + picture_name + "_scaled.imgdat", "w+") as f:
                f.write(writeImageData(img))
            
            del img 

#Try opening the given path as a file
opened = True
try:
    image_file = open(image_path)
    img = Image.open(image_file)
except:
    opened = False

#Open as a URL if the file did not work
if opened is False:
    try:
        r = request.urlopen(image_path)
        img = Image.open(r)
    except URLError:
        print("There was a protocol error")
        quit()
    except SyntaxError:
        print("Invalid format for url")
        quit()
    except:
        print("There was a problem with the given image")
        quit()

#Convert the image into a 3 by 3 image
size = 3,3
img = img.resize(size, Image.NEAREST)

#Get the pixels in this image
pixels = getPixels(img)

#Compare to the other scaled images to see if there is a match
for scaled_image in glob.glob(path_of_script + folder_name + "*"):
    with open(scaled_image, encoding = "ISO-8859-1") as f:
        count = 0
        match = True
        
        content = f.readlines()
        filePixels = getPixelsFromFile(content)

        print("file pixels")
        print(filePixels)
        print("pixels")
        print(pixels)
    
        for pixel in filePixels:
            if pixel != pixels[count]:
                match = False
                break
            count += 1
        if match:
            print("ITS A MATCH")
