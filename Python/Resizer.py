# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 15:29:17 2022
@author: Patri
"""

import os
import cv2

# Function to resize image, keeping aspect ratio
# (c) @thewaywewere - https://stackoverflow.com/questions/44650888/resize-an-image-without-distortion-opencv
def image_resize(image, width = None, height = None, inter = cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv2.resize(image, dim, interpolation = inter)

    # return the resized image
    return resized

# Parameters
_read_directory = "C:\\Users\\Patri\\Desktop\\Inpsyde"
_new_Directory = "C:\\Users\\Patri\\Desktop\\Inpsyde\\edited2\\"
_wanted_Width = 925     #370 * 2.5 for better resolution
_wanted_Height = 500    #200 * 2.5

# Loop over every file (maybe change this to only go for pics?)
for filename in os.listdir(_read_directory):
    f = os.path.join(_read_directory, filename)
    # Checking if it is a file and not a folder
    if os.path.isfile(f) and filename != "desktop.ini":
        #print("working on: " + f)
        # Read the file
        img = cv2.imread(f, cv2.IMREAD_UNCHANGED)
        # Resize it, assuming that the pic is in portrait, maybe todo for landscape
        img = image_resize(img, height = _wanted_Height)
        # Get theshape of the image
        (img_height, img_width) = img.shape[:2]
        # Calc how large the borders have to be
        left_border = int((_wanted_Width - img_height) / 2)
        right_border = _wanted_Width - img_width - left_border
        # Convert Image to BGRA (if not already in correct format)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
        # If image shape is wrong, borders will have negative size, leading to an error, just avoiding it here
        if(left_border >= 0 and right_border >= 0):
            # Create a border on image
            img = cv2.copyMakeBorder(img, 0, 0, left_border, right_border, cv2.BORDER_CONSTANT, value =[0,0,0,0])
            # Write image
            cv2.imwrite(_new_Directory + filename[0:-4] + ".png", img)
        else:
            # Skip image if shape is wrong
            print("Error [Wrong Shape], Skipping Image: " + f)

