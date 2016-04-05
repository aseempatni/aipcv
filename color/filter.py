import cv2
import csv
import math
from color import *
from matplotlib import pyplot as plt
import pprint as pp

# Get the white point
white_point_x, white_point_y = RGB_to_xy(255,255,255)
white_point_x, white_point_y = 1.0/3,1.0/3

# Reference line for finding angles
x_ref = 0
y_ref = -1

# Dot product of two vectors
def dot(vA, vB):
    return vA[0]*vB[0]+vA[1]*vB[1]

# Get angle from reference line for a given point
def get_angle(x,y):
    global white_point_x, white_point_y, x_ref, y_ref
    vA = [x_ref,y_ref]
    vB = [x-white_point_x, y-white_point_y]
    vC = [-y_ref,x_ref]

    # Get dot prod
    dot_prod = dot(vA, vB)

    # Get magnitudes
    magA = dot(vA, vA)**0.5
    magB = dot(vB, vB)**0.5

    if magA == 0 or magB == 0:
        return 0
    # Get angle in radians and then convert to degrees
    angle = math.acos(dot_prod/magB/magA)

    # Basically doing angle <- angle mod 360
    ang_deg = math.degrees(angle)%360

    if dot(vB,vC)<0:
        # As in if statement
        return 360 - ang_deg
    else:
        return ang_deg

# Convert wavelength range to angle range
def wavelength_to_angle_range(wl_min, wl_max):
    return wavelength_angle[wl_max], wavelength_angle[wl_min]

# Filter a pixel if it comes within the angle range
def filter_pixel(pixel,angle_min,angle_max):
    x,y = RGB_to_xy(pixel[2], pixel[1], pixel[0])
    angle = get_angle(x,y)
    if angle > angle_min and angle < angle_max:
        return True
    else:
        return False

def parse_chromaticity_chart(filename):
    wavelength_angle = {}
    with open(filename,'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        lines = []
        for row in spamreader:
            lines.append(row)
        # global x_ref, y_ref
        # last = lines[-1]
        # x,y = RGB_to_xy(last[1],last[2], last[3])
        # x_ref = x-white_point_x
        # y_ref = y-white_point_y
        # print x_ref, y_ref

        for row in lines:
            #print ', '.join(row)
            x,y = XYZ_to_xy(float(row[1]), float(row[2]), float(row[3]))
            angle = get_angle(x,y)
            wavelength_angle[int(row[0])] = angle
            # print row, angle, x, y
    return wavelength_angle

# FIlter the image for a wavelength range
def filter_wavelength(img,wl_min, wl_max):
    # Convert wavelength range to angle range
    img_orig = img.copy()
    angle_min, angle_max = wavelength_to_angle_range(wl_min, wl_max)
    print angle_min, angle_max

    # Filter the pixels falling in the angle range
    for i in range(img.shape[0]):    # for every pixel:
        for j in range(img.shape[1]):
            if filter_pixel(img[i,j],angle_min, angle_max):
                img[i,j] = [0,0,0]

    return img

#------------------------------------------#
# Parse required files
#------------------------------------------#

# Parse chromaticity chart
wavelength_angle = parse_chromaticity_chart("ciexyz31_1.csv")

if __name__ == "__main__":
    myDictionary = wavelength_angle
    plt.plot(myDictionary.keys(), myDictionary.values(), 'b--')
    plt.xlabel('Wavelength')
    plt.ylabel('Angle')
    plt.title('Wavelength Angle in Chromaticity Chart')
    plt.show()
