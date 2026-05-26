'''
Parameter file for CloudCam options.
'''

import typing

# CloudCam.py
min_median: typing.Final[float] = 40  # Lower limit for median value
max_median: typing.Final[float] = 100  # Upper limit for median value
step_size: typing.Final[float] = 0.60  # Exposure scaling step size, %
expose: typing.Final[float] = 1  # Set starting exposure
max_exp: typing.Final[float] = 10
gain: typing.Final[float] = 1  # Set starting gain
gainmax: typing.Final[float] = 5

# Cloud_Graph.py
scale_img: typing.Final[bool] = True  # Toggle image scaling
binary_erosion: typing.Final[bool] = False  # Toggle binary erosion filtering
rotate: typing.Final[int] = -12  # How much to rotate the image

# Cloud_Mask.py
radius: typing.Final[int] = 500  # large aperture mask radius, pixels
x_center: typing.Final[int] = 525  # Center pixel on x axis 512
y_center: typing.Final[int] = 670  # Center pixel on y axis 670
