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
                k1[i,j] = h
                k2[i,j] = h
                # Need to handle this part properly.
                # I have no idea how does the expressiion h*h -k become negative.

                # print i,j
                # print h*h -k
                # print h,k

                continue

    return k1,k2

# Get the surface type at a point from the h and k values.
def surface_type_from_kh(img,H,K):
    surface = np.zeros((img.shape[0], img.shape[1],3))
    for i in range(len(surface)):
        for j in range(len(surface[0])):
            h = H[i,j]
            k = K[i,j]
            if k<0:
                if h<0:
                    surface[i,j] = (255,0,0)
                if h==0:
                    surface[i,j] = (0,255,0)
                if h>0:
                    surface[i,j] = (0,0,255)
            if k==0:
                if h<0:
                    surface[i,j] = (255,255,0)
                if h==0:
                    surface[i,j] = (255,0,255)
                if h>0:
                    surface[i,j] = (0,255,255)
            if k>0:
                if h<0:
                    surface[i,j] = (50,255,255)
                if h==0:
                    surface[i,j] = (50,255,255)
                if h>0:
                    surface[i,j] = (50,255,255)
    return surface

# # Get the surface type at a point from the h and k values.
# def surface_type_from_kh(img,H,K):
#     surface = np.zeros((img.shape[0], img.shape[1]))
#     for i in range(len(surface)):
#         for j in range(len(surface[0])):
#             h = H[i,j]
#             k = K[i,j]
#             if k<0:
#                 if h<0:
#                     surface[i,j] = 0
#                 if h==0:
#                     surface[i,j] = 40
#                 if h>0:
#                     surface[i,j] = 80
#             if k==0:
#                 if h<0:
#                     surface[i,j] = 120
#                 if h==0:
#                     surface[i,j] = 160
#                 if h>0:
#                     surface[i,j] = 200
#             if k>0:
#                 if h<0:
#                     surface[i,j] = 220
#                 if h==0:
#                     surface[i,j] = 240
#                 if h>0:
#                     surface[i,j] = 255
#     return surface

# Get the surface type at a point from the h and k values.
def surface_type_from_principal(img,H,K):
    surface = np.zeros((img.shape[0], img.shape[1],3))
    for i in range(len(surface)):
        for j in range(len(surface[0])):
            h = H[i,j]
            k = K[i,j]
            if k<0:
                if h<0:
                    surface[i,j] = (255,0,0)
                if h==0:
                    surface[i,j] = (0,255,0)
                if h>0:
                    surface[i,j] = (0,0,255)
            if k==0:
                if h<0:
                    surface[i,j] = (255,255,0)
                if h==0:
                    surface[i,j] = (255,0,255)
                if h>0:
                    surface[i,j] = (0,255,255)
            if k>0:
                if h<0:
                    surface[i,j] = (50,255,255)
                if h==0:
                    surface[i,j] = (50,255,255)
                if h>0:
                    surface[i,j] = (50,255,255)
    return surface

def normalize_matrix(m):
    min = m[0,0]
    max = m[0,0]
    for i in range(len(m)):
        for j in range(len(m[0])):
            if min>m[i,j]:
                min = m[i,j]
            if max<m[i,j]:
                max = m[i,j]
    for i in range(len(m)):
        for j in range(len(m[0])):
            m[i,j]-=min
            m[i,j]*=255/(max-min)
    return m

# Input image
img = cv2.imread(image_name,0)


def display(img):
    # Show image
    cv2.imshow("image",img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

#-------------------------------#
# Compute Curvature
#-------------------------------#

# Compute gaussian and mean curvatures from depth image
K,H = gaussian_mean_curvature(img)
print K
print H

# Compute principal curvatures from gaussian and mean curvatures
k1,k2 = principal_curvature(H,K)
print k1
print k2


#K = normalize_matrix(K)
#display(K)

#-------------------------------#
# Characterise local topology
#-------------------------------#


# Characterise local topology at a point based on signs of curvature

# (a) Based on Principal Curvature
surface_from_principal = surface_type_from_principal(img,k1,k2)
display(surface_from_principal)

# (b) Based on gaussian and mean curvature
surface_from_hk = surface_type_from_kh(img,H,K)
display(surface_from_hk)


# Perform region growing of homogeneous labels




