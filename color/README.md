python

1. Filtering
To filter the image `image2.jpg` for blue color, run:
`python filter_driver.py <image> <min_wavelength> <max_wavelength>`
`python filter_driver.py image2.jpg 450 495`

if no range is given, then the range data is taken from range.txt
For example, run
`python filter_driver.py <image>`
`python filter_driver.py image2.jpg `

2. Normalised Histogram
python hist.py <image>
`python hist.py <image>`
`python hist.py color_images/20160201_173719.jpg`

3. K Means
`python kmeans.py`
