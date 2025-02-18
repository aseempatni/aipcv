import cv2
import numpy as np
from matplotlib import pyplot as plt
from sfm import *
import sys

# Configuration parameters are taken as command line arguments

# Parsing arguments

# Image 1 name
image_1_name = sys.argv[1]

# Image 2 name
image_2_name = sys.argv[2]

# Method used for finding corresponding points
# 1. sift
# 2. manual
# 3. data
method = sys.argv[3]

count1 = 1
count2 = 1

# Mouse Callback used to select corresponding points

def draw_circle(event,x,y,flags,param):
    global img1,img2, count1, count2, pts1, pts2
    if event == cv2.EVENT_LBUTTONDBLCLK:
        if param==1:
            cv2.putText(img1,str(count1),(x,y),cv2.FONT_HERSHEY_SIMPLEX, 1,(0,0,0),2)
            count1 +=1
            pts1.append((x,y))
        elif param==2:
            cv2.putText(img2,str(count2),(x,y),cv2.FONT_HERSHEY_SIMPLEX, 1,(0,0,0),2)
            count2 +=1
            pts2.append((x,y))

        print x,y

img1orig = cv2.imread(image_1_name)  #queryimage # left image
img2orig = cv2.imread(image_2_name) #trainimage # right image

# Resizing both the images

img1 = cv2.resize(img1orig, (700,700))
img2 = cv2.resize(img2orig, (700,700))

def save_points(pts1, pts2, filename1, filename2):
    np.save(filename1, pts1)
    np.save(filename2, pts2)

def load_points(filename1, filename2):
    pts1 = np.load(filename1)
    pts2 = np.load(filename2)
    return pts1, pts2

good = []
pts1 = []
pts2 = []

#----------------------------------------#
# Findiing corresponding points
#----------------------------------------#

# Method 1: Using SIFT

if (method=="sift"):

    sift = cv2.xfeatures2d.SIFT_create()

    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(img1,None)
    kp2, des2 = sift.detectAndCompute(img2,None)

    # FLANN parameters
    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks=50)

    flann = cv2.FlannBasedMatcher(index_params,search_params)
    matches = flann.knnMatch(des1,des2,k=2)

    # ratio test as per Lowe's paper
    for i,(m,n) in enumerate(matches):
        if m.distance < 0.8*n.distance:
            good.append(m)
            pts2.append(kp2[m.trainIdx].pt)
            pts1.append(kp1[m.queryIdx].pt)

    # We select only inlier points
    # pts1 = pts1[mask.ravel()==1]
    # pts2 = pts2[mask.ravel()==1]


# Method 2: Using manual selection

elif (method=="manual"):

    # Display both the images to manually select the corresponding points in them

    cv2.namedWindow('First Image')
    cv2.setMouseCallback('First Image',draw_circle,param=1)
    cv2.namedWindow('Second Image')
    cv2.setMouseCallback('Second Image',draw_circle,param=2)
    while(1):
        cv2.imshow('Second Image',img2)
        cv2.imshow('First Image',img1)
        if cv2.waitKey(20) & 0xFF == 27:
            break

    cv2.destroyAllWindows()

    save_points(pts1, pts2, "pts1","pts2")

# Method 3: Use data from saved numpy file

else:

    pts1,pts2 = load_points("pts1.npy","pts2.npy")


pts1 = np.int32(pts1)
pts2 = np.int32(pts2)

#----------------------------------------#
# Computing fundamental Matrix
#----------------------------------------#

F, mask = cv2.findFundamentalMat(pts1,pts2,cv2.FM_LMEDS)
np.set_printoptions(suppress=True)
print "Fundamental Matrix is"
print F

print "Fundamental Matrix as computed by DLT is"
F2 = compute_fundamental(pts1, pts2)
print F2

# Visualizing epipolar lines of the feature points used in the computation

def drawlines(img1,img2,lines,pts1,pts2):
    ''' img1 - image on which we draw the epilines for the points in img2
        lines - corresponding epilines '''
    r,c,colors = img1.shape
    #img1 = cv2.cvtColor(img1,cv2.COLOR_GRAY2BGR)
    #img2 = cv2.cvtColor(img2,cv2.COLOR_GRAY2BGR)
    for r,pt1,pt2 in zip(lines,pts1,pts2):
        color = tuple(np.random.randint(0,255,3).tolist())
        x0,y0 = map(int, [0, -r[2]/r[1] ])
        x1,y1 = map(int, [c, -(r[2]+r[0]*c)/r[1] ])
        img1 = cv2.line(img1, (x0,y0), (x1,y1), color,1)
        img1 = cv2.circle(img1,tuple(pt1),5,color,-1)
        img2 = cv2.circle(img2,tuple(pt2),5,color,-1)
    return img1,img2

# Find epilines corresponding to points in right image (second image) and
# drawing its lines on left image
lines1 = cv2.computeCorrespondEpilines(pts2.reshape(-1,1,2), 2,F)
lines1 = lines1.reshape(-1,3)
img5,img6 = drawlines(img1,img2,lines1,pts1,pts2)

# Find epilines corresponding to points in left image (first image) and
# drawing its lines on right image
lines2 = cv2.computeCorrespondEpilines(pts1.reshape(-1,1,2), 1,F)
lines2 = lines2.reshape(-1,3)
img3,img4 = drawlines(img2,img1,lines2,pts2,pts1)
#cv2.imshow('First Image',img5)
#cv2.waitKey(0)
#cv2.imshow('First Image',img3)
#cv2.waitKey(0)

#----------------------------------------#
# Epipoles of a fundamental matrix
#----------------------------------------#
right_epipole = compute_epipole(F)
left_epipole = compute_epipole(np.transpose(F))

print "Left epipole is ", left_epipole
print "Right epipole is ", right_epipole

# Visualizing the position of both the epipoles

img7 = cv2.circle(img5,tuple(right_epipole[0:2].astype(int)),10,(0,0,0),)-1
cv2.imshow('Right Epipole',img7)
cv2.waitKey(0)
img7 = cv2.circle(img3,tuple(left_epipole[0:2].astype(int)),10,(0,0,0),)-1
cv2.imshow('Right Epipole',img7)
cv2.waitKey(0)


#----------------------------------------#
# Camera matrix estimation from F
#----------------------------------------#
P1 = np.array([[1,0,0,0],[0,1,0,0],[0,0,1,0]])
P2 = compute_P_from_fundamental(F)

print "P1 is assumed [I|O]"
print P1
print "P2 is computed as"
print P2
R = np.zeros((3,3))
cv2.RQDecomp3x3(P2[0:3,0:3], R)
print "Camera calibration matrix is"
print R

#----------------------------------------#
# Determine 3D Point
#----------------------------------------#

x = np.transpose(pts1)
x = np.vstack([x,np.ones(x.shape[1])])
print "Points from first image are"
print np.transpose(x)

y = np.transpose(pts2)
y = np.vstack([y,np.ones(y.shape[1])])
print "Points from second image are"
print np.transpose(y)

pts3d = triangulate(x, y, P1, P2)
pts3d = np.transpose(pts3d)
print "points in 3d"
print pts3d


plt.subplot(121),plt.imshow(img5)
plt.subplot(122),plt.imshow(img3)
plt.show()


