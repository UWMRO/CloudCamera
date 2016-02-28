'''
Test code for Cloud Camera histogram plotting
Used to determine the mean value of each row in an image
to be used for later analysis
'''

__author__ = "J. Matt Armstrong"
__copyright__ = "NA"
__credits__ = ["Nathen Nguyen"]
__license__ = "GPL"
__version__ = "0.1"
__maintainer__ = "J. Matt Armstrong"
__email__ = "jmarmstr@uw.edu"
__status__ = "Developement"

import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt
import time
from logger import *
import os


class CloudGraph(object):
	def __init__(self):
		self.l = Logger() #Logger class creates logfile of processes
		self.dir = '/Images'
		self.fakeOut =  False # Boolean value that if set to True, will test code using
							  # a set of test images, rather than taking new image
		self.logType = 'cloud' # Parameter used in  Logger class to create logfile

	def pixel_value_list(self, image):
		result = []
		for row in range(len(image)):
			for pixel in image[row]:
				#print pixel
				result.append(pixel)
		return result

	def plot_histogram(self, pixel_list):
		plt.clf()
		plt.hist(pixel_list, bins = 50, normed = True)
		plt.show()

	def fits_to_list(self, file_name):
		hdulist = fits.open(file_name)
		return hdulist[0].data
		hdulist.close()

if __name__=="__main__":
	cg = CloudGraph()
	test = [[1,2,1],[4,4,6],[9,9,9]]
	#pix_list = cg.pixel_value_list(test)
	#cg.plot_histogram(pix_list)
	img = cg.fits_to_list("20160221T205857_30.fits")
	img_list = cg.pixel_value_list(img)
	cg.plot_histogram(img_list)
