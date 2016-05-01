import cv2
import numpy as np
import sys
import matplotlib.pyplot as plt
from utils import * 

if __name__ == '__main__':
	img_blur = cv2.imread(sys.argv[1])
	img_blur = cv2.resize(img_blur, (0,0), fx=0.25, fy=0.25)
	
	img1 = cv2.imread(sys.argv[2])
	img1 = cv2.resize(img1, (0,0), fx=0.25, fy=0.25)
	
	img2 = cv2.imread(sys.argv[3])
	img2 = cv2.resize(img2, (0,0), fx=0.25, fy=0.25)
		
	M1 = getHomography(img_blur,img1)
	M2 = getHomography(img_blur,img2)

	img1_tr = cv2.warpPerspective(img1, M1, (img_blur.shape[1],img_blur.shape[0]))
	img2_tr = cv2.warpPerspective(img2, M2, (img_blur.shape[1],img_blur.shape[0]))

	img2gray = cv2.cvtColor(img1_tr,cv2.COLOR_BGR2GRAY)
	ret, mask1_inv = cv2.threshold(img2gray, 10, 255, cv2.THRESH_BINARY_INV)

	img2gray = cv2.cvtColor(img2_tr,cv2.COLOR_BGR2GRAY)
	ret, mask2_inv = cv2.threshold(img2gray, 10, 255, cv2.THRESH_BINARY_INV)

	dst = cv2.bitwise_and(img_blur,img_blur, mask = mask1_inv)
	dst = cv2.add(dst, img1_tr)

	dst = cv2.bitwise_and(dst,dst, mask = mask2_inv)
	dst = cv2.add(dst, img2_tr)

	cv2.imshow("Ajanta 1 image", img1)
	cv2.imshow("Ajanta 2 image", img2)
	cv2.imshow("Ajanta Blurred image", img_blur)
	cv2.imshow("Final Image", dst)
	cv2.imwrite(sys.argv[1].split('.')[0]+"_restored.jpg",dst)
	cv2.waitKey(0)