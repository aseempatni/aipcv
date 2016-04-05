import cv2
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
    if X+Y+Z==0:
        return 0,0
    return X/(X+Y+Z), Y/(X+Y+Z)

def RGB_to_xy(R,G,B):
    X,Y,Z = RGB_to_XYZ(R,G,B)
    return XYZ_to_xy(X,Y,Z)

def bgr_to_rgb(bgr_img):
    b,g,r = cv2.split(bgr_img)       # get b,g,r
    rgb_img = cv2.merge([r,g,b])     # switch it to rgb
    return rgb_img


