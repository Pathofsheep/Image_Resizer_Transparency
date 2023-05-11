# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 15:29:17 2022
@author: Patri
"""

import os
import cv2


# Function to resize image, keeping aspect ratio
# (c) @thewaywewere - https://stackoverflow.com/questions/44650888/resize-an-image-without-distortion-opencv
def image_resize(image, _width=None, _height=None):
    # Get the size of the image
    (_img_height, _img_width) = image.shape[:2]

    # If no argument is given, return the original image
    if _width is None and _height is None:
        return image

    if _height is not None:
        # Calculate the resize ratio for the new width
        _ratio = _height / float(_img_height)
        # The new dimensions is the new width and the given height
        _dim = (int(_img_width * _ratio), _height)

    else:
        # Calculate the resize ratio for the new height
        _ratio = _width / float(_img_width)
        # The new dimensions is the new height and the given width
        _dim = (_width, int(_img_height * _ratio))

    # Return the resized image
    return cv2.resize(image, _dim, interpolation=cv2.INTER_AREA)


# Parameters
debug = True
read_directory = r"H:\Meine Ablage\Work\2023_05_11"
new_Directory = read_directory + "\\edited\\"
wanted_width = 733
wanted_height = 500
operation = "Crop"
# operation = "Borders"

# Loop over every file (maybe change this to only go for pics?)
# Currently ignoring any folders
for filename in os.listdir(read_directory):
    f = os.path.join(read_directory, filename)
    # Checking if it is a file and not a folder.
    # Possible todo: Check if file extension is an actual image
    if os.path.isfile(f) and filename != "desktop.ini":
        if debug:
            print("Working on:\t\t" + f)
        # Read the file
        img = cv2.imread(f, cv2.IMREAD_UNCHANGED)
        # Get the shape of the image to determine where borders have to be placed
        (img_height, img_width) = img.shape[:2]

        # If Operation is set to Borders, resize the image to fit the frame and add transparent borders
        if operation == "Borders":
            prefix = "rsz_"
            # Resize it depending on image ratio
            if (img_height / img_width) >= (wanted_height / wanted_width):
                # If height ratio of original image is bigger than wanted height ratio,
                # adjust height. Else adjust width.
                img = image_resize(img, _height=wanted_height)
            else:
                img = image_resize(img, _width=wanted_width)
            # Get the new shape of the image
            (img_height, img_width) = img.shape[:2]
            if debug:
                print("New image res:\t" + str(img_width) + "x" + str(img_height))
            # Calc how large the borders have to be
            left_border = int((wanted_width - img_width) / 2)
            right_border = wanted_width - img_width - left_border
            top_border = int((wanted_height - img_height) / 2)
            bottom_border = wanted_height - img_height - top_border

            if debug:
                print("Border size:\t" + str(left_border + right_border) + "x" +
                      str(top_border + bottom_border))

            # Convert Image to BGRA incase it's not already in correct format
            img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)

            # Create a border on the sides of the image
            img = cv2.copyMakeBorder(img, top_border, bottom_border, left_border,
                                     right_border, cv2.BORDER_CONSTANT, value=[0, 0, 0, 0])

        # If Operation is set to Crop, just crop the image symmetrically to fit the correct ratio
        elif operation == "Crop":
            prefix = "crp_"
            if debug:
                print("Old image size:\t" + str(img_width) + "x" + str(img_height))
            if (img_height / img_width) >= (wanted_height / wanted_width):
                # If height ratio of original image is bigger, crop the height.
                cropped_height = int((wanted_height / wanted_width) * img_width)
                crop_border = int((img_height - cropped_height) / 2)
                if debug:
                    print("New image size:\t" + str(img_width) + "x" + str(cropped_height))
                img = img[crop_border: img_height - crop_border, ]
            else:
                # Else crop the width.
                cropped_width = int((wanted_width / wanted_height) * img_height)
                crop_border = int((img_width - cropped_width) / 2)
                if debug:
                    print("New image size:\t" + str(cropped_width) + "x" + str(img_height))
                img = img[0:img_height, crop_border: img_width - crop_border]
        else:
            # Wrong operation has been set
            raise ValueError('Invalid operation chosen.')

        # Create dir if it doesn't yet exist
        if not os.path.exists(new_Directory):
            os.mkdir(new_Directory)
        # And finally, save the image with prefix in directory
        if debug:
            print("Writing file:\t" + new_Directory + r'\\' + prefix + filename[0:-4] + ".png")
        cv2.imwrite(new_Directory + prefix + filename[0:-4] + ".png", img)
