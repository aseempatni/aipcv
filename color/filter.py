import cv2
import csv
import math
import sys

from matplotlib import pyplot as plt

#------------------------------------------#
# Color Space Conversion
#------------------------------------------#

def RGB_to_XYZ(R,G,B):
    var_R = float( R )/ 255         # R from 0 to 255
    var_G = float( G )/ 255         # G from 0 to 255
    var_B = float( B )/ 255         # B from 0 to 255

    if ( var_R > 0.04045 ) :
        var_R = ( ( var_R + 0.055 ) / 1.055 ) ** 2.4
    else:
        var_R = var_R / 12.92
    if ( var_G > 0.04045 ) :
        var_G = ( ( var_G + 0.055 ) / 1.055 ) ** 2.4
    else:
        var_G = var_G / 12.92
    if ( var_B > 0.04045 ) :
        var_B = ( ( var_B + 0.055 ) / 1.055 ) ** 2.4
    else:
        var_B = var_B / 12.92

    var_R = var_R * 100
    var_G = var_G * 100
    var_B = var_B * 100

    X = var_R * 0.4124 + var_G * 0.3576 + var_B * 0.1805
    Y = var_R * 0.2126 + var_G * 0.7152 + var_B * 0.0722
    Z = var_R * 0.0193 + var_G * 0.1192 + var_B * 0.9505

    return X,Y,Z

def XYZ_to_xy(X,Y,Z):
    return X/(X+Y+Z), Y/(X+Y+Z)

def RGB_to_xy(R,G,B):
    X,Y,Z = RGB_to_XYZ(R,G,B)
    return XYZ_to_xy(X,Y,Z)

def bgr_to_rgb(bgr_img):
    b,g,r = cv2.split(bgr_img)       # get b,g,r
    rgb_img = cv2.merge([r,g,b])     # switch it to rgb
    return rgb_img

#------------------------------------------#
#------------------------------------------#

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
            x,y = RGB_to_xy(row[1], row[2], row[3])
            angle = get_angle(x,y)
            wavelength_angle[int(row[0])] = angle
            # print row[0], angle
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
            if not filter_pixel(img[i,j],angle_min, angle_max):
                img[i,j] = [0,0,0]

    # Plot both the images
    plt.subplot(121),plt.imshow(bgr_to_rgb(img_orig))
    plt.subplot(122),plt.imshow(bgr_to_rgb(img))
    #plt.show()
    return img

wl_min = 450
wl_max = 490

#------------------------------------------#
# Parse required files
#------------------------------------------#

# Parse chromaticity chart
wavelength_angle = parse_chromaticity_chart("ciexyz31_1.csv")

# Parse range data from file
wl_ranges = []
with open("range.txt",'r') as range_data:
    for line in range_data:
        wl_ranges.append( line.strip().split(' '))

# Read the image
img = cv2.imread("image2.jpg")

# Read the wavelength parameters from the CLI
if len(sys.argv) >2:
    wl_min = int(sys.argv[1])
    wl_max = int(sys.argv[2])
    img1 =  filter_wavelength(img.copy(),wl_min, wl_max)
    plt.subplot(121),plt.imshow(bgr_to_rgb(img))
    plt.subplot(122),plt.imshow(bgr_to_rgb(img1))
    plt.show()
    exit()

#------------------------------------------#
# Filtering
#------------------------------------------#

# Filter image for each wavelength range
images = []
for wl_range in wl_ranges:
    wl_min = int(wl_range[0])
    wl_max = int(wl_range[1])
    images.append( filter_wavelength(img.copy(),wl_min, wl_max) )

#------------------------------------------#
# Visualisation
#------------------------------------------#

# Plot the filtered images
plt.subplot(241),plt.imshow(bgr_to_rgb(img))
plt.subplot(242),plt.imshow(bgr_to_rgb(images[0]))
plt.subplot(243),plt.imshow(bgr_to_rgb(images[1]))
plt.subplot(244),plt.imshow(bgr_to_rgb(images[2]))
plt.subplot(245),plt.imshow(bgr_to_rgb(images[3]))
plt.subplot(246),plt.imshow(bgr_to_rgb(images[4]))
plt.subplot(247),plt.imshow(bgr_to_rgb(images[5]))
plt.show()

