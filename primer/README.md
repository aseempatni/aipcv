Initial parts are trivial

### Salt and pepper noise

`python noise.py`

### Sobel

`python sobel.py ../lego.tif`

`python sobel.py ../lego.tif library`

### DCT

Run manual implementation using `python dct.py ../cap.bmp`

While viewing multiple images in same frame in openCV, the quality decreases. So, we can manually open the inverse transformed image and the actual image to compare.

### Harris corner detection

Run manual Implementation using `python harris.py ../lego.tif`

Run library Implementation using `python harris.py ../lego.tif library`
