To run the code,

`python fundamental.py <img1> <img2> <mode>`

eg `python fundamental.py DSC_0244.jpg DSC_0245.JPG sift`

The two images will be displayed then.
Select the corresponding points in both the images in the same order. The index will be displayed on the image.
We need to select at least 8 points.

G`

Mode can be:
sift
manual
data

### Sift mode:

`python fundamental.py DSC_0244.jpg DSC_0245.JPG sift`

The corresponding points are automatically selected using SIFT.

### Manual mode:

The two images will be displayed.
Select the corresponding points in both the images in the same order. The index will be displayed on the image.
We need to select at least 8 points.
After selecting the required number of corresponding points press ESC to proceed.

### Data mode:

`python fundamental.py DSC_0246.JPG DSC_0247.JPG data`

The data for corresponding points will be taken from a previously saved numpy data file.
This mode is primarily for speeding up the testing process. The manual or sift mode is recommended for the demo prupose.

The required computations will be done and then both the images with epipoles and epilines will be displayed.
The fundamental matrix, 3d coordinates, projection matrix and calibration matrix will be logged on console.
