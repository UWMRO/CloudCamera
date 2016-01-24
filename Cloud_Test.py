'''
Test code for Cloud Camera image acquisition
Used to collect test images with a variety of exposure times
for later analysis and proseccing
'''

__author__ = "J. Matt Armstrong"
__copyright__ = "NA"
__credits__ = ["Joseph Huehnerhoff"]
__license__ = "GPL"
__version__ = "0.1"
__maintainer__ = "NA"
__email__ = "jmarmstr@uw.edu"
__status__ = "Developement"

import numpy as np
from astropy.io import fits
import subprocess
from camera import *
import thread
import time
from logger import *
import os


class CloudCam(object):
	def __init__(self):
		self.c = CameraExpose() # CameraExpose object, used to take images
		self.l = Logger() #Logger class creates logfile of processes
		self.dir = '/home/matt/College/AUEG/CloudCam/'
		self.dir = os.getcwd()
		self.expTime = 0 # Image exposure time in seconds, used when calling the
		# CameraExpose object to take images.
		self.fakeOut =  False # Boolean value that if set to True, will test code using
		# a set of test images, rather than taking new images
		self.currentImage = 2 # Integer used in testing, tracks how many images have been taken
		self.logType = 'cloud' # Parameter used in  Logger class to create logfile


	# Runs through a loop, taking images with different exposure times
	# Will complete num loops, each time taking exp images
	# Increasing the exposure time by 1 second until exp is reached.
	# Saves each image with as timestamp_exposure.fits
	'''
	def CloudExpose(self, num, exp):
	    print 'Exposing '+num+' images, with exposure times up to '+exp+' seconds.'
	    for i in range[1,num,1]:
	        for j in range[exp]:
	            name = time.strftime('%Y%m%dT%H%M%S')+'_'+str(j)+'.fits'
	            c.expose(name=name, exp=j)
	            print 'Exposing for '+str(j)+' seconds, file name: '+name
	    print 'Exposure loop complete.'
'''
	# Runs through a loop, taking bias images with 0 second exposure time
	# Saves each image as bias_timestamp.fits
	def CloudBias(self, num):
		print 'Collecting '+str(num)+' bias images'
		for i in range(1,num,1):
			self.refName = "bias_" + time.strftime("%Y%m%dT%H%M%S") + ".fits"
			self.expTime = 0.5
			self.takeImage('bias', self.refName, self.expTime, self.dir)
			print 'Bias routine complete'

	def takeImage(self, imType = None, imgName = None, imExp = None, imDir = None):
	        """Takes the class, a string keyword for image type, a string for image
        	name, an integer for exposure tiem, and a string for directory name.
        	The function checks if the variable fakeOut is equal to true first
        	-- if so, ends function and carries out rest of code using existing
        	images.  If not, the function takes an image using the CameraExpose
        	object defined in the constructor, and checks that the image has
        	been taken and saved.
        	Args:
        	    imType (str): the type of image (bias, dark, object)
        	    imgName (str): the name of the image
        	    imExp (str): the exposure length in seconds
        	    imDir (str):  the directory of the image to be saved
        	Returns:
        	    int.
        	    0 -- image was taken
        	    1 -- image not taken
        	    2 -- unknown state
        	Raises:
        	    Exception
        	"""
		#cam = CameraExpose()  you instantiate this above as self.c
		l = Logger()
		self.fakeOut =  False
		im = False
		if self.fakeOut != True:
			im = self.c.runExpose(imgName, imExp, imDir)
			#l.logStr('Image\t%s %s %s' % (str(imgName), str(imExp), str(imDir)), self.logType)
			if im == True: # check on completion and save of image exposure
				return 0
			else:
				raise Exception("Image exposure not completed")
				return 1
		else:
			return 3 # Simply returns if no exception raised

if __name__ == '__main__':

	cam = CloudCam()
	# Calls the CloudBias function to collect bias imagery for later reduction.
	cam.CloudBias(17)

	# Calls the CloudExpose function, will produce num*exp images.
	#CloudExpose(num=2, exp=5)
	print 'Camera Routine Complete'
