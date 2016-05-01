## Instructions to use

### Compute curvatures

To compute the principal, gaussian and mean curvatures at each point of the range image, characterize local topology and perform region growing, run:
`python main.py <range_image_name>`
For example,
`python main.py RGBD/1.png`

### Perform region growing of homogeneous labels.

Regoin growing clubs the pixels having the same label. This is done using BFS. The resultant image shows the different regions with different intencities.

## Quality of segmentation

### Observations:

By comparing with the corresponding RGB images, we observe that:

* We found that (a) and (b) both gave a similar performance, with principal curvature performing slightly better.
* Also, the combination of a and b i.e. (a,b) is found to give better segmentation than using just the gaussian, mean or principal curvatures alone.
* The results are almost the same for the different range images.
* The segments are not that clearly visible in the output, and most of them are of really small size.
* The reason for that could be poor recording of the range data.

### Result:

(a) = (b) < (a,b)
