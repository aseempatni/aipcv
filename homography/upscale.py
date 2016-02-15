import cv2
import numpy as np
import sys
import matplotlib.pyplot as plt
from utils import * 

def getByte(value, n):
	return (value >> (n*8) & 0xFF)

def getpixel(img, x, y, ch):
	return img[y][x][ch]

def lerp( s,  e,  t):
	return s + (e - s) * t

def blerp( c00,  c10,  c01,  c11,  tx,  ty):
	return lerp(lerp(c00, c10, tx), lerp(c01, c11, tx), ty)

def interpolate(img_src, scalex,scaley):
	height, width = img_src.shape[:2]
	newH = height * scaley
	newW = width * scalex
	dst = np.zeros((newH,newW,3),np.uint8)
	x = 0
	y = 0
	while(y < newH):
		if x >= newW:
			x = 0 
			y += 1
		if y>= newH:
			return dst
		for ch in range(3):
			gx = x * (width - 1) / float(newW)
			gy = y * (height - 1) / float(newH)
			gxi = int(gx)
			gyi = int(gy)
			result = 0
			c00 = int(getpixel(img_src, gxi, gyi, ch))
			c10 = int(getpixel(img_src, gxi+1, gyi, ch))
			c01 = int(getpixel(img_src, gxi, gyi+1, ch))
			c11 = int(getpixel(img_src, gxi+1, gyi+1, ch))
			for i in range(3):
				result |= int(blerp(getByte(c00, i), getByte(c10, i), getByte(c01, i), getByte(c11, i), gx - gxi, gy - gyi)) << (8*i)
			dst[y][x][ch] = result
		x += 1
	return dst


if __name__ == '__main__':

	img1 = cv2.imread(sys.argv[1])
	img1 = cv2.resize(img1, (0,0), fx=0.25, fy=0.25)
	
	img2 = cv2.imread(sys.argv[2])
	img2 = cv2.resize(img2, (0,0), fx=0.25, fy=0.25)
		
	origH,origW = img1.shape[:2]
	img1_interpolate = interpolate(img1,2,2)
	M = getHomography(img1,img2) # img1_interpolate = M(img2)
	img2_proj = cv2.warpPerspective(img2, M, ( img1.shape[1] , img1.shape[0]))
	img_out = np.copy(img1_interpolate)

	height, width = img_out.shape[:2]

	for i in range(height):
		for j in range(width):
			if int(img_out[i][j][0]) + int(img_out[i][j][1]) + int(img_out[i][j][2]) < int(img2_proj[i/2][j/2][0]) + int(img2_proj[i/2][j/2][1]) + int(img2_proj[i/2][j/2][2]):
				img_out[i][j][0] = img2_proj[i/2][j/2][0]
				img_out[i][j][1] = img2_proj[i/2][j/2][1]
				img_out[i][j][2] = img2_proj[i/2][j/2][2]
	
	cv2.imshow("Original Image", img1)
	cv2.imshow("Projected Image", img2_proj)
	cv2.imshow("interpolated Image", img1_interpolate)
	cv2.imshow("interpolated Image Modified", img_out)
	cv2.imwrite(sys.argv[1] + "_upscaled.jpg",img_out)
	cv2.waitKey(0)
