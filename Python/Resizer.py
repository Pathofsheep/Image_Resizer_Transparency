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
_read_directory = "C:\\Users\\Patri\\Desktop\\BENELUX NEW\\Products additional\\"
_new_Directory = "C:\\Users\\Patri\\Desktop\\BENELUX NEW\\Products additional\\edited\\"
_wanted_Width = 925     #370 * 2.5 for better resolution
_wanted_Height = 500    #200 * 2.5

# Loop over every file (maybe change this to only go for pics?)
# Currently ignoring any folders
for filename in os.listdir(_read_directory):
    f = os.path.join(_read_directory, filename)
    # Checking if it is a file and not a folder
    if os.path.isfile(f) and filename != "desktop.ini":
        print("working on: " + f)
        # Read the file
        img = cv2.imread(f, cv2.IMREAD_UNCHANGED)
        # Get the shape of the image to determine where borders have to be placed
        (img_height, img_width) = img.shape[:2]
        # Resize it depending on image ratio
        if img_height / img_width <= _wanted_Height / _wanted_Width:
            img = image_resize(img, width=_wanted_Width)
        else:
            img = image_resize(img, height=_wanted_Height)
        # Get the new shape of the image
        (img_height, img_width) = img.shape[:2]
        # Calc how large the borders have to be
        left_border = int((_wanted_Width - img_width) / 2)
        right_border = _wanted_Width - img_width - left_border
        top_border = int((_wanted_Height - img_height) / 2)
        bottom_border = _wanted_Height - img_height - top_border

        # Convert Image to BGRA (if not already in correct format)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)

        # Create a border on the sides of the image
        img = cv2.copyMakeBorder(img, top_border, bottom_border, left_border,
                                 right_border, cv2.BORDER_CONSTANT, value=[0, 0, 0, 0])
        # Create dir if it doesn't yet exist
        if not os.path.exists(_new_Directory):
            os.mkdir(_new_Directory)
        # Write image
        cv2.imwrite(_new_Directory + filename[0:-4] + ".png", img)