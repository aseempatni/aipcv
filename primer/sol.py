import numpy as np
import cv2
import random
from matplotlib import pyplot as plt
from math import log
import math

# Load image 1
cap = cv2.imread('cap.bmp',0)
# cv2.imshow('image',cap)
# cv2.waitKey(0)

# Load image 2
lego = cv2.imread('lego.tif')

graylego = cv2.cvtColor(lego,cv2.COLOR_BGR2GRAY)
'''
cv2.imshow('image',img)
cv2.waitKey(0)

# convert pixel to grayscale
def weightedAverage(pixel):
    return 0.299*pixel[0] + 0.587*pixel[1] + 0.114*pixel[2]

# convert color image to grayscale
for rownum in range(len(img)):
    for colnum in range(len(img[rownum])):
         img[rownum,colnum] = weightedAverage(img[rownum,colnum])

# show grayscale converted image
cv2.imshow('image',img)
cv2.waitKey(0)
'''

def sp_noise(image,prob):

# Add salt and pepper noise to image
# prob: Probability of the noise

	prob = prob/2
	output = np.zeros(image.shape,np.uint8)
	thres = 1 - prob
	for i in range(image.shape[0]):
	    for j in range(image.shape[1]):
	        rdn = random.random()
	        if rdn < prob:
	            output[i][j] = 0
	        elif rdn > thres:
	            output[i][j] = 255
	        else:
	            output[i][j] = image[i][j]
	return output


def median_filter(image,type,window_width,window_height):
	output = np.zeros(image.shape,np.uint8)
	image_width = image.shape[0]
	image_height = image.shape[1]

   	window = np.zeros(window_width * window_height)
   	edgex = (window_width / 2)
   	edgey = (window_height / 2)
   	for x in range(edgex, image_width - edgex):
		for y in range (edgey, image_height - edgey):
		   	i = 0
		   	for fx in range (0 , window_width):
				for fy in range(0 , window_height):
					window[i] = image[x + fx - edgex,y + fy - edgey]
					i = i + 1
		   	if type=="mean":
		   		output[x,y] = np.mean(window)
		   	elif type=="median":
		   		output[x,y] = np.median(window)

	return output

def filtering(OriginalImage,p):

	print "p =",p
	noisyimg = sp_noise(OriginalImage,p)

	medianfilteredimg = median_filter(noisyimg,"median",10,10)
	# cv2.imshow('Median Filtered Image',medianfilteredimg)
	# cv2.waitKey(0)

	meanfilteredimg = median_filter(noisyimg,"mean",10,10)
	# cv2.imshow('Mean Filtered Image',meanfilteredimg)
	# cv2.waitKey(0)

	mse = ((OriginalImage - medianfilteredimg) ** 2).mean(axis=None)
	psnr = 20* log(255,10) - 10*log(mse,10)
	print "Median PSNR =",psnr

	mse = ((OriginalImage - meanfilteredimg) ** 2).mean(axis=None)
	psnr = 20* log(255,10) - 10*log(mse,10)
	print "PMean SNR =",psnr

	titles = ['Original Image', 'Added Noise Image',
	            'Median filtering', 'Mean Filtering']
	images = [OriginalImage, noisyimg, medianfilteredimg, meanfilteredimg]

	for i in xrange(4):
	    plt.subplot(2,2,i+1),plt.imshow(images[i],'gray')
	    plt.title(titles[i])
	    plt.xticks([]),plt.yticks([])

	plt.savefig("Noise Filtering.png")
	plt.show()

def noise():
	ps = [0.01,0.02,0.05,0.1,0.2,0.3,0.5,0.7,0.9]
	for p in ps:
		filtering(cap,p)

if __name__ == "__main__":
	p = 0.5
	filtering(cap,p)