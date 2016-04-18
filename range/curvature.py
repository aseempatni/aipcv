import cv2

import math
import numpy as np
import sys

image_name = sys.argv[1]

# Get gaussian and mean curvatures from range image
def gaussian_mean_curvature(Z):
    Zy, Zx = np.gradient(Z)
    Zxy, Zxx = np.gradient(Zx)
    Zyy, _ = np.gradient(Zy)
    K = (Zxx * Zyy - (Zxy ** 2)) /  (1 + (Zx ** 2) + (Zy **2)) ** 2
    H = (Zx**2 + 1)*Zyy - 2*Zx*Zy*Zxy + (Zy**2 + 1)*Zxx
    H = -H/(2*(Zx**2 + Zy**2 + 1)**(1.5))
    return K,H

# Get principal curvatures from gaussian and mean curvatures
def principal_curvature(H,K):
    k1 = np.zeros(img.shape)
    k2 = np.zeros(img.shape)
    for i in range(len(K)):
        for j in range(len(K[0])):

            h = H[i,j]
            k = K[i,j]

            try:
                k1[i,j] = h + math.sqrt(h*h - k)
                k2[i,j] = h - math.sqrt(h*h - k)

            except:

                # Need to handle this part properly.
                # I have no idea how does the expressiion h*h -k become negative.

                # print i,j
                # print h*h -k
                # print h,k

                continue

    return k1,k2

# Get the surface type at a point from the h and k values.
def surface_type_from_kh(k,h):
    if k<0:
        if h<0:
            return "peak"
        if h==0:
            return "none"
        if h>0:
            return "pit"
    if k==0:
        if h<0:
            return "ridge"
        if h==0:
            return "flat"
        if h>0:
            return "valley"
    if k>0:
        if h<0:
            return "suddle ridge"
        if h==0:
            return "minimal surface"
        if h>0:
            return "saddle valley"


# Input image
img = cv2.imread(image_name,0)

# Show image
# cv2.imshow("image",img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# Compute gaussian and mean curvatures from depth image
K,H = gaussian_mean_curvature(img)
print K
print H

# Compute principal curvatures from gaussian and mean curvatures
k1,k2 = principal_curvature(H,K)
print k1
print k2

# Characterise local topology at a point based on signs of curvature

