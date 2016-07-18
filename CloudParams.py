'''
Parameter file for CloudCam options.


'''

#CloudCam.py
min_median = 40			#Lower limit for median value
max_median = 100		#Upper limit for median value
step_size = 0.40		#Exposure scaling step size, %
expose = 1			#Set starting exposure
gain = 1			#Set starting gain

#Cloud_Graph.py
scale_img = True		#Toggle image scaling
binary_erosion = False		#Toggle binary erosion filtering
rotate = 112			#How much to rotate the image

#Cloud_Mask.py
radius = 500			#large aperture mask radius, pixels
x_center = 512			#Center pixel on x axis
y_center = 640			#Center pixel on y axis

