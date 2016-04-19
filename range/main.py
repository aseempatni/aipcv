from curvature import *
import sys

image_name = sys.argv[1]

# Input image
img = cv2.imread(image_name,0)

#-------------------------------#
# Compute Curvature
#-------------------------------#

# Compute gaussian and mean curvatures from depth image
K,H = gaussian_mean_curvature(img)

# Compute principal curvatures from gaussian and mean curvatures
k1,k2 = principal_curvature(H,K)

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

# Regoin grouping is done using BFS, and the result is same as the image obtained in surface type from curvatures.

