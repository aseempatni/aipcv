import numpy as np
import cv2

# Read image and convert to grayscale
lego = cv2.imread('lego.tif')
graylego = cv2.cvtColor(lego,cv2.COLOR_BGR2GRAY)


# Harris Corner Detection Library Implementation

img = lego

gray = graylego
gray = np.float32(gray)

dst = cv2.cornerHarris(gray,2,3,0.04)

# result is dilated for marking the corners, not important
dst = cv2.dilate(dst,None)

# Threshold for an optimal value, it may vary depending on the image.
img[dst>0.01*dst.max()]=[0,0,255]

cv2.imshow('dst',img)
if cv2.waitKey(0) & 0xff == 27:
    cv2.destroyAllWindows()


# TODO: Manual Implementation

