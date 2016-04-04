from filter import *
from matplotlib import pyplot as plt
import sys

#------------------------------------------#
# Parse required files
#------------------------------------------#

# Parse range data from file
wl_ranges = []
with open("range.txt",'r') as range_data:
    for line in range_data:
        wl_ranges.append( line.strip().split(' '))

# Default configuration
wl_min = 450
wl_max = 490
image_name = "image1.jpg"

# Read the image
image_name = sys.argv[1]
img = cv2.imread(image_name)

# Read the wavelength parameters from the CLI
if len(sys.argv) >3:
    wl_min = int(sys.argv[2])
    wl_max = int(sys.argv[3])
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

