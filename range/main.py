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

K = normalize_matrix(K)
display(K,"Gaussian Curvature")
display(H,"Mean Curvature")

#-------------------------------#
# Characterise local topology
#-------------------------------#

# Characterise local topology at a point based on signs of curvature

# (a) Based on Principal Curvature
# surface contains labels as 1,2,3...
surface_from_principal = surface_type_from_principal(img,k1,k2)

# (b) Based on gaussian and mean curvature
# surface contains labels as 1,2,3...
surface_from_hk = surface_type_from_hk(img,H,K)

#-------------------------------#
# Regoin Growing
#-------------------------------#

# Regoin grouping is done using BFS, and the result is same as the image obtained in surface type from curvatures.

# Using only case a

# surface image is scaled visualisation for surface, with segments being marked.
surface_image_from_principal = scale_surface_to_image(surface_from_principal)
display(surface_image_from_principal,"Surface Labels/segments using only Principal Curvature")

# Using only case b

# surface image is scaled visualisation for surface, with segments being marked.
surface_image_from_hk = scale_surface_to_image(surface_from_hk)
display(surface_image_from_hk,"Surface labels/segments using only Gaussian and Mean Curvatures")

# Using both case a and b

surface_image_from_hk_principal = scale_hk_principal_surface_to_image(surface_from_hk, surface_from_principal)
display(surface_image_from_hk_principal,"Surface labels/segments using all the curvatures.")
