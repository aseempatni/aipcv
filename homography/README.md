## Instructions to use

### Fronto-rectilinear View

To get the output in default resolution:
`python homo.py text_box.jpg`

To get the output image in user specified resolution

`python homo.py <image> <x-res> <y-res>`

For example:
`python homo.py text_box.jpg 90 160`

Steps:
* After running the code, the image will be displayed. 
* Left click on the four corner points in normal order, ie. top left, top right, bottom left and then bottom right.
* Then press any key to proceed.
* The final image will be displayed and saved in the same directory as `text_box_rectilinear.jpg`.


### Image mosaicing

`python mosaic.py <image-1> <image-2>`

For example:
`python mosaic.py Ajanta_1.jpg Ajanta_2.jpg`

Output stored in `Ajanta_1_mosaic.jpg`


### Deblurring

`python blur.py <image_blurred> <image-1> <image-2>`

For example:
`python blur.py Ajanta_blurred.jpg Ajanta_1.jpg Ajanta_2.jpg`

Output stored in `Ajanta_blurred_restored.jpg`


### Upscaling

`python mosaic.py <image-1> <image-2>`

For example:
`python mosaic.py Ajanta_1.jpg Ajanta_2.jpg`

Output stored in `Ajanta_1_mosaic.jpg`


## Technique and Discussions

### Fronto-rectilinear View

It is simply obtained by taking the four corner points as input and computing a homography to transform the four points into four corner points of the final image.
The results obtained are acceptable.

### DeBlurring

* Deblurring is done by computing a homography to transform the sharp image to the blurred image, and then masking it over the blurred image.
* There are some problems observed here, as the different images are taken under different lighting conditions.

### Mosaicing

* Mosaicing is done by computing a homography from the first image to the second one. The the transformed first image is masked on to the second image. The uniion of these two images gives the mosaiced image.
* There is a slight shift while capturing the two images, so mild distortion is observed in the output image. Also there are differences in illumination intensity.

### Upscaling

* Upscaling is done by adding more pixels, precisely 4 time the pixel for each pixel. Then the intermediate pixels are interpolated from the surrounding pixels. This is the standard technique used for upscaling. On top of that, I used the information from other image of the same scene to fill out some pixels. If the information isn't available then the interpolated values are used.
* Here also, similar problems of illumination intensity are objerved.