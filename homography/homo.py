#!/usr/bin/env python

import cv2
import numpy as np
import sys

filename = sys.argv[1]

# Read source image.
im_src = cv2.imread(filename)

if len(sys.argv)>2:
    final_width = int(sys.argv[2])
    final_height = int(sys.argv[3])
else:
    final_width=im_src.shape[1]
    final_height=im_src.shape[0]

# I'm too lazy to convert right click to left click
#the [x, y] for each right-click event will be stored here
right_clicks = list()

#this function will be called whenever the mouse is right-clicked
def mouse_callback(event, x, y, flags, params):

    #right-click event value is 2
    if event == 1:
        global right_clicks

        #store the coordinates of the right-click event
        right_clicks.append([x, y])

        #this just verifies that the mouse data is being collected
        #you probably want to remove this later
        print right_clicks


if __name__ == '__main__' :

    cv2.namedWindow(filename, cv2.WINDOW_NORMAL)
    cv2.setMouseCallback(filename, mouse_callback)
    print "Please left click on the 4 corner points in normal flow order."
    cv2.imshow(filename, im_src)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Four corners of the book in source image
    #pts_src = np.array([[0, 0], [0, 159], [400, 0],[400, 400]])
    pts_src = np.array(right_clicks)

    # Read destination image.
    im_dst = blank_image = np.zeros((final_height,final_width,3), np.uint8)
    # Four corners of the book in destination image.
    pts_dst=np.array([[0,0],[final_width,0],[0,final_height],[final_width,final_height]])

    # Calculate Homography
    h, status = cv2.findHomography(pts_src, pts_dst)

    # Warp source image to destination based on homography
    im_out = cv2.warpPerspective(im_src, h, (im_dst.shape[1],im_dst.shape[0]))

    # Display image
    cv2.imshow("Warped Source Image", im_out)
    cv2.imwrite(sys.argv[1]+'_rectilinear.jpg',im_out)
    cv2.waitKey(0)
