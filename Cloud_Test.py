'''
Test code for Cloud Camera image acquisition
Used to collect test images with a variety of exposure times
for later analysis and processing
'''

__author__ = "J. Matt Armstrong"
__copyright__ = "NA"
__credits__ = ["Joseph Huehnerhoff"]
__license__ = "GPL"
__version__ = "0.2"
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
		#self.dir = '/home/matt/College/AUEG/CloudCam/'
		self.dir = '/home/matt/College/mro_guide/Camera/images'
		self.expTime = 0 # Image exposure time in seconds, used when calling the
						 # CameraExpose object to take images.
		self.fakeOut =  False # Boolean value that if set to True, will test code using
							  # a set of test images, rather than taking new images
		self.currentImage = 2 # Integer used in testing, tracks how many images have been taken
		self.logType = 'cloud' # Parameter used in  Logger class to create logfile



	def CloudExpose(self, num, exp, step):
		""" Runs through a loop, taking images with different exposure times
		Will complete num loops, each time taking exp images
		Increasing the exposure time by 1 second until exp is reached.
		Saves each image with as timestamp_exposure.fits"""
		stepexpose = exp / step
		print 'Imaging '+str(num)+' loops, with exposure times up to '+str(exp)+' seconds with '+str(step)+' second step between exposures.'
		for i in range(num):
			for j in range(int(stepexpose)):
				name = time.strftime('%Y%m%dT%H%M%S')+'_'+str((j+1)*step)+'.fits'
				print 'Exposing for '+str((j+1)*step)+' seconds, file name: '+name
	        		self.takeImage('image', name, ((j+1)*step), self.dir)
	         	print 'Exposure loop '+str(i)+' complete.'


	def CloudBias(self, num):
		"""Runs through a loop, taking bias images with 0 second exposure time
		Saves each image as bias_timestamp.fits"""

		print 'Collecting '+str(num)+' bias images'
		for i in range(1,num,1):
			self.refName = "bias_" + time.strftime("%Y%m%dT%H%M%S") + ".fits"
			self.expTime = 0
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
		l = Logger()
		self.fakeOut =  False
		im = False
		if self.fakeOut != True:
			im = self.c.runExpose(imgName, imExp, imDir)
			l.logStr('Image\t%s %s %s' % (str(imgName), str(imExp), str(imDir)), self.logType)
			if im == True: # check on completion and save of image exposure
				time.sleep(1)
				return 0
			else:
				raise Exception("Image exposure not completed")
				return 1
		else:
			return 3 # Simply returns if no exception raised

if __name__ == '__main__':

	cam = CloudCam()
	# Calls the CloudBias function to collect bias imagery for later reduction.
	cam.CloudBias(1)

	# Calls the CloudExpose function, will produce num*exp images with a step size for exposure.
	"""
	exp=60, step=5 : Run time = 7mins
	"""
	"""
	cam.CloudExpose(num=1, exp=0.1, step=5)
	print 'Camera Routine Complete'
	"""
