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
from PIL import Image
import itertools
import sys

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

	def mask(self, pixel_list):
		median = np.median(pixel_list)
		#print median
		result = pixel_list

		for i in range(len(pixel_list)):
			if pixel_list[i] > (2 * median):
				result[i] = median
			elif pixel_list[i] < (median / 2):
				result[i] = median
			else:
				result[i] = pixel_list[i]

		return result
	def masked_img(self, image, mask_val):
		result = []
		median = np.median(image)
		for row in range(len(image)):
			temp_row = []
			for pixel in image[row]:
				if pixel > (int(mask_val) * median):
					temp_row.append(median)
				elif pixel < (median / int(mask_val)):
					temp_row.append(median)
				else:
					temp_row.append(pixel)
			result.append(temp_row)
		return result

	def plot_histogram(self, pixel_list):
		plt.clf()
		plt.hist(pixel_list, bins = (max(pixel_list) - min(pixel_list)), normed = True)
		plt.show()

	def fits_to_list(self, file_name):
		hdulist = fits.open(file_name)
		return hdulist[0].data
		hdulist.close()

	def array_to_png(self, file_path, pixel_grid):
		size = len(pixel_grid[0]), len(pixel_grid)
		image = Image.new("L", size)

		#print "Writing", size[0], 'x', size[1], "image to file", file_path

	    # Flatten the list by making an iterable sequence over the inner lists
	    # and then materializing the whole list.
		data = list(itertools.chain.from_iterable(pixel_grid))
		image.putdata(data)

		try:
			# Write the image. File extension of file_path determines
			# the encoding.
			image.save(file_path)
		except IOError as e:
			print e
		except:
			print "Unexpected error writing file", file_path

if __name__=="__main__":
	cg = CloudGraph()
	#test = [[1,2,1],[4,4,6],[9,9,9]]
	#pix_list = cg.pixel_value_list(test)
	#cg.plot_histogram(pix_list)
	img = cg.fits_to_list("20160101T220024.fits")
	#img_list = cg.pixel_value_list(img)
	#cg.plot_histogram(img_list)
	#masked = cg.mask(img_list)
	#time.sleep(2)
	masked_img = cg.masked_img(img, 2)
	#cg.plot_histogram(masked)
	cg.array_to_png("test.png", img)
	cg.array_to_png("test_masked.png", masked_img)
