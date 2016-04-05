import cv2
import numpy as np
from matplotlib import pyplot as plt
import sys
from filter import *
import numpy as np

def plot_histogram(img):
    color = ('b','g','r')
    for i,col in enumerate(color):
        histr = cv2.calcHist([img],[i],None,[256],[0,256])
        plt.plot(histr,color = col)
        plt.xlim([0,256])
    plt.show()

angle_wavelength = {v: k for k, v in wavelength_angle.items()}
wavelengths = wavelength_angle.keys()
angles = angle_wavelength.keys()

def find_nearest(array,value):
    idx = (np.abs(array-value)).argmin()
    return array[idx]

def angle_to_wavelength(angle):
    global angles
    nearest_angle = find_nearest(np.array(angles), angle)
    return angle_wavelength[nearest_angle]

def pixel_to_angle(pixel):
    x,y = RGB_to_xy(pixel[2], pixel[1], pixel[0])
    angle = get_angle(x,y)
    return angle

def get_pixel_wavelength(pixel):
    angle = pixel_to_angle(pixel)
    wavelength = angle_to_wavelength(angle)
    return wavelength

def black_or_white(pixel):
    if pixel[0] == 0 and pixel[1] == 0 and pixel[2] == 0:
        return True
    if pixel[0] == 255 and pixel[1] == 255 and pixel[2] == 255:
        return True
    if pixel[0] == pixel[1] and pixel[2] == pixel[1]:
        return True
    return False

def image_histogram(img):
    data = []
    hist = {}
    for wl in wavelengths:
        hist[wl] = 0
    for i in range(img.shape[0]):    # for every pixel:
        for j in range(img.shape[1]):
            if not black_or_white(img[i,j]):
                wavelength = get_pixel_wavelength(img[i,j])
                if wavelength !=360 and wavelength != 830:
                    data.append(wavelength)
                # if wavelength == 829:
                #     print img[i,j]
                hist[wavelength] = hist[wavelength] + 1
    return data


if __name__ == "__main__":
    image_name = sys.argv[1]
    # Read the image
    img = cv2.imread(image_name)

    img = cv2.resize(img, (500,img.shape[1]*500/img.shape[0]))
    hist = image_histogram(img)
    data = hist
    #print hist

    # Plot histogram
    myDictionary = hist
    #plt.plot(myDictionary.keys(), myDictionary.values(), 'b--')
    #plt.plot(myDictionary.keys(), myDictionary.values(), 'bo-')
    n, bins, patches = plt.hist(data, 470, normed=1, facecolor='g', alpha=0.75)
    plt.xlabel('Wavelength')
    plt.ylabel('Frequency')
    plt.title('Normalised Histogram')
    plt.show()# plot_histogram(img)

# filter_wavelength(img, 360,830)

# plot_histogram(img)
