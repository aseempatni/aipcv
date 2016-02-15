import cv2
import numpy as np

def getHomography(img1,img2):
	sift = cv2.xfeatures2d.SIFT_create()
	kp1, des1 = sift.detectAndCompute(img1,None)
	kp2, des2 = sift.detectAndCompute(img2,None)
	# FLANN parameters
	FLANN_INDEX_KDTREE = 0
	index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
	search_params = dict(checks = 50)   # or pass empty dictionary
	flann = cv2.FlannBasedMatcher(index_params,search_params)
	good = []
	matches = flann.knnMatch(des2,des1,k = 2)
	for m,n in matches:
		if m.distance < 0.7*n.distance:
			good.append(m)
	if len(good) > 4:
		src_pts = np.float32([ kp2[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
		dst_pts = np.float32([ kp1[m.trainIdx].pt for m in good ]).reshape(-1,1,2)

		M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
		return M

	return 0
