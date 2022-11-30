# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 15:29:17 2022
@author: Patri
"""

import os
import cv2

#Function to resize image, keeping aspect ratio
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


_read_directory = "C:\\Users\\Patri\\Desktop\\Inpsyde"
_new_Directory = "C:\\Users\\Patri\\Desktop\\Inpsyde\\edited2\\"
_wanted_Width = 740
_wanted_Height = 400

for filename in os.listdir(_read_directory):
    f = os.path.join(_read_directory, filename)
    # checking if it is a file
    if os.path.isfile(f) and filename != "desktop.ini":
        #print("working on: " + f)
        #Read the file
        img = cv2.imread(f , cv2.IMREAD_UNCHANGED)
        #Resize it
        #!! THIS ASSUMES THAT WE ARE CREATING BORDERS ON THE SIDE, NOT ON TOP
        img = image_resize(img,height = _wanted_Height)
        #Get Imags Height and Width
        (h, w) = img.shape[:2]
        #Get Borders Dimensions
        left_border = int((_wanted_Width - int(w)) / 2)
        right_border = _wanted_Width - w - left_border
        #exit if, if theres a negative value
        if(left_border >= 0 and right_border >= 0):
            #Create a black border on image
            img2 = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
            img2 = cv2.copyMakeBorder(img2, 0, 0, left_border, right_border, cv2.BORDER_CONSTANT, value =[0,0,0,0])
            img = cv2.copyMakeBorder(img, 0, 0, left_border, right_border, cv2.BORDER_CONSTANT, value =[0,0,0,0])
            #Convert it to gray, to filter out the background and make it transparent
            tmp = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            #Set threshold for Alpha channel (Transparency)
            _,alpha = cv2.threshold(tmp,0,255,cv2.THRESH_BINARY)
            #Split channels of the image
            
            if(len(cv2.split(img)) == 3):
                b, g, r = cv2.split(img)
            elif(len(cv2.split(img)) == 4):
                b, g, r, a_dummy = cv2.split(img)
            else:
                print("error, wrong dims")
                
            #Create a List of the images channels
            rgba = [b, g, r, alpha]
            #Merge the channels back to an image
            new_image = cv2.merge(rgba,4)
            #Write image
            print(filename)
            cv2.imwrite(_new_Directory + filename[0:-4] + ".png", new_image)
        else:
            print("Error on Image: " + f)



cv2.imwrite(_new_Directory+"edit.png", img2)
