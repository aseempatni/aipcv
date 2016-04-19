import cv2

import math
import numpy as np

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
    k1 = np.zeros(H.shape)
    k2 = np.zeros(H.shape)
    for i in range(len(K)):
        for j in range(len(K[0])):
            h = H[i,j]
            k = K[i,j]
            k1[i,j] = h + math.sqrt(max(0,h*h - k))
            k2[i,j] = h - math.sqrt(max(0,h*h - k))
    return k1,k2

# Get the surface type at a point from the k1 and k2 values.
def surface_type_from_principal(img,H,K):
    surface = np.zeros((img.shape[0], img.shape[1]))
    for i in range(len(surface)):
        for j in range(len(surface[0])):
            h = H[i,j]
            k = K[i,j]
            if k<0:
                if h<0:
                    surface[i,j] = 1
                if h==0:
                    surface[i,j] = 2
                if h>0:
                    surface[i,j] = 3
            if k==0:
                if h<0:
                    surface[i,j] = 2
                if h==0:
                    surface[i,j] = 5
                if h>0:
                    surface[i,j] = 6
            if k>0:
                if h<0:
                    surface[i,j] = 3
                if h==0:
                    surface[i,j] = 6
                if h>0:
                    surface[i,j] = 4
    return surface

# Get the surface type at a point from the h and k values.
def surface_type_from_hk(img,H,K):
    surface = np.zeros((img.shape[0], img.shape[1]))
    for i in range(len(surface)):
        for j in range(len(surface[0])):
            h = H[i,j]
            k = K[i,j]
            if k<0:
                if h<0:
                    surface[i,j] = 1
                if h==0:
                    surface[i,j] = 2
                if h>0:
                    surface[i,j] = 3
            if k==0:
                if h<0:
                    surface[i,j] = 4
                if h==0:
                    surface[i,j] = 5
                if h>0:
                    surface[i,j] = 6
            if k>0:
                if h<0:
                    surface[i,j] = 7
                if h==0:
                    surface[i,j] = 8
                if h>0:
                    surface[i,j] = 9
    return surface

# scale surface labels, which can then be displayed as an image
def scale_surface_to_image(surface):
    surface = surface * 25
    return surface.astype(np.uint8)

# Get an image using surface labels from both gaussian, mean and principal curvatures.
def scale_hk_principal_surface_to_image(hk,principal):
    img = np.zeros((hk.shape[0], hk.shape[1],3))
    hk = hk * 25
    principal = principal * 25
    for i in range(hk.shape[0]):
        for j in range(hk.shape[1]):
            # img[i,j,1] = hk[i,j]
            # img[i,j,2] = principal[i,j]
            img[i,j] = [0,hk[i,j],principal[i,j]]
    return img.astype(np.uint8)

# Normalize a matrix, which can then be displayed as an image
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
    return m.astype(np.uint8)

# Utility function to display an image
def display(img,image_name = "image"):
    # Show image
    cv2.imshow(image_name,img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

