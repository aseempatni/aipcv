import cv2
import numpy as np
import sys
import matplotlib.pyplot as plt
from utils import *

if __name__ == '__main__':

	img1 = cv2.imread(sys.argv[1])
	img1 = cv2.resize(img1, (0,0), fx=0.25, fy=0.25)
	
	img2 = cv2.imread(sys.argv[2])
	img2 = cv2.resize(img2, (0,0), fx=0.25, fy=0.25)
		
	M = getHomography(img1,img2) # img1 = M(img2)
	img2_out = cv2.warpPerspective(img2, M, ( 2*img1.shape[1] , img1.shape[0]))

	rows,cols,channels = img1.shape
	
	roi = img2_out[0:rows,0:cols]
	img2gray = cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)
	ret, mask = cv2.threshold(img2gray, 10, 255, cv2.THRESH_BINARY)
	mask_inv = cv2.bitwise_not(mask)
	
	bg = cv2.bitwise_and(roi,roi,mask = mask_inv)
	fg = cv2.bitwise_and(img1,img1,mask = mask)
		
	dst = cv2.add(bg,fg)
	img2_out[0:rows,0:cols] = dst

	cv2.imshow("Image 1", img1)
	cv2.imshow("Image 2", img2)
	cv2.imshow("Output Image", img2_out)
	cv2.imwrite(sys.argv[1]+"_mosaic.jpg", img2_out)
	cv2.waitKey(0)