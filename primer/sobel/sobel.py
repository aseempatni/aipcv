import numpy as np
import cv2

from matplotlib import pyplot as plt
import math

import sys

if (len(sys.argv) < 2):
    print("Pass the path to input file as an argument")
    exit()
input_image_file = sys.argv[1]

# Read image
lego = cv2.imread(input_image_file,0)

def execute_library_function(img):
	laplacian = cv2.Laplacian(img,cv2.CV_64F)
	sobelx = cv2.Sobel(img,cv2.CV_64F,1,0,ksize=5)
	cv2.imwrite("X_Gradient_library.png",sobelx)
	sobely = cv2.Sobel(img,cv2.CV_64F,0,1,ksize=5)
	cv2.imwrite("Y_Gradient_library.png",sobely)

	plt.subplot(2,2,1),plt.imshow(img,cmap = 'gray')
	plt.title('Original'), plt.xticks([]), plt.yticks([])
	plt.subplot(2,2,2),plt.imshow(laplacian,cmap = 'gray')
	plt.title('Laplacian'), plt.xticks([]), plt.yticks([])
	plt.subplot(2,2,3),plt.imshow(sobelx,cmap = 'gray')
	plt.title('Sobel X'), plt.xticks([]), plt.yticks([])
	plt.subplot(2,2,4),plt.imshow(sobely,cmap = 'gray')
	plt.title('Sobel Y'), plt.xticks([]), plt.yticks([])

	plt.show()

if (len(sys.argv) >2):
	if (sys.argv[2]=="library"):
		print "Using library implementation"
		execute_library_function(lego)
	else:
		print "Improper syntax"
	exit()



def sobel():
	# Original Image
	# cv2.imshow('image',lego)
	# cv2.waitKey(0)
	
	# X gradient image
	A = [[-1,0,1],[-2,0,2],[-1,0,1]]
	gradx = convolve(A,lego)
	# cv2.imwrite("X_Gradient.png",gradx)
	# cv2.imshow('X gradient',gradx)
	# cv2.waitKey(0)

	# Y gradient image
	A = [[-1,-2,-1],[0,0,0],[1,2,1]]
	grady = convolve(A,lego)
	# cv2.imwrite("Y_Gradient.png",grady)
	# cv2.imshow('Y Gradient',grady)
	# cv2.waitKey(0)

	# Gradient magnitude image
	gradmag = gradmagnitude(lego,gradx, grady)
	print gradmag
	cv2.imwrite("Gradient Magnitude.png", gradmag)
	cv2.imshow('Gradient Magnitude',gradmag)
	cv2.waitKey(0)
	
	thresh = threshold(gradmag,250)
	cv2.imshow('Gradient Magnitude',thresh)
	cv2.imwrite("Gradient Magnitude Thresholded.png", thresh)
	exit()
	# Displaying all side by side
	titles = ['X gradient', 'Y gradient',
	            'Gradient Magnitude', 'Original']
	images = [gradx, grady, gradmag, lego]

	for i in xrange(4):
	    plt.subplot(2,2,i+1),plt.imshow(images[i],'gray')
	    plt.title(titles[i])
	    plt.xticks([]),plt.yticks([])

	plt.savefig("gradient.eps")
	plt.show()

def convolve(A,image):

	output = np.zeros(image.shape,np.uint8)
	image_width = image.shape[0]
	image_height = image.shape[1]
	window_width = 3
	window_height = 3
   	edgex = (window_width / 2)
   	edgey = (window_height / 2)
	for x in range(edgex, image_width - edgex):
		for y in range (edgey, image_height - edgey):
		   	i = 0
		   	for fx in range (0 , window_width):
				for fy in range(0 , window_height):
					i = i + image[x + fx - edgex,y + fy - edgey]*A[fx][fy]
			output[x,y] = i/4
	return output

def threshold(gradient, t):
	for x in range(gradient.shape[0]):
		for y in range(gradient.shape[1]):
			if gradient[x,y]> t:
				gradient[x,y] = 255
			else:
				gradient[x,y] = 0

	return gradient

def gradmagnitude(image,gradx, grady):

	output = np.zeros(image.shape,np.int)
	image_width = image.shape[0]
	image_height = image.shape[1]

	for x in range(0, image_width ):
		for y in range (0, image_height ):
			# print gradx[x,y]*gradx[x,y] + grady[x,y]*grady[x,y] 
			output[x,y] = math.sqrt(gradx[x,y]*gradx[x,y] + grady[x,y]*grady[x,y] )
			# print output[x,y], gradx[x,y], grady[x,y]
			output[x,y] = (abs(gradx[x,y]) + abs(grady[x,y]))/2
			# output[x,y]/=2

	return output

if __name__ == "__main__":
	sobel()