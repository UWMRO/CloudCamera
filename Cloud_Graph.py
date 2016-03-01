'''
Test code for Cloud Camera histogram plotting
Used to determine the mean value of each row in an image
to be used for later analysis
'''

__author__ = "J. Matt Armstrong"
__copyright__ = "NA"
__credits__ = ["Nathen Nguyen", "Joseph Huehnerhoff"]
__license__ = "GPL"
__version__ = "0.2"
__maintainer__ = "J. Matt Armstrong"
__email__ = "jmarmstr@uw.edu"
__status__ = "Developement"

import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
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
		self.logType = 'cloud' # Parameter used in  Logger class to create logfile

	def pixel_value_list(self, image):
		'''
		Produce two arrays, the first is a list of the pixel values
		and the second is the number of pixels at that value
		'''
		#Trying to use numpy histogram to improve processing speed.
		result = np.histogram(image, bins = np.arange(np.amax(image)+1))
		return result

		'''
		These were functions used for testing how to mask the image, saved for
		future use.

	def mask(self, pixel_list):
		median = np.median(pixel_list)
		std = np.std(pixel_list)
		#print median
		result = pixel_list

		for i in range(len(pixel_list)):
			if pixel_list[i] > (2 * median):
				result[i] = 0
			elif pixel_list[i] < (median / 2):
				result[i] = 0
			else:
				result[i] = pixel_list[i]
		return result

	def masked_img(self, image, mask_val):
		result = []
		median = np.median(image)
		std = np.std(image)
		print std
		for row in range(len(image)):
			temp_row = []
			for pixel in image[row]:
				if pixel > ((mask_val) * std):
					temp_row.append(0)
				elif pixel < (std / (mask_val)):
					temp_row.append(0)
				else:
					temp_row.append(pixel)
			result.append(temp_row)
		return result
		'''

	def masked_img2(self, image, radius):
		'''
		This function combines multiple masking steps into one function.
		First it finds the median and standard deviation of the image
		Next it goes through each image row and examines the pixel value
		If the pixel is outside of the radius, it is turned black
		If the pixel is above or below a threshold related to the standard deviation
			it is set to 0
		Finally, any pixels left have their values increased by 1 to raise them above the mask value

		The output image is the masked image.
		'''
		result = []
		std = 3*(np.std(image))
		median = np.median(image)
		for x in range(len(image)):
			temp_row = []
			shift_x = x-(1024/2)
			for y in range(len(image[x])):
				row = image[x]
				shift_y = y-(1280/2)
				if np.sqrt((shift_x)**2 + (shift_y)**2) > radius:
					temp_row.append(0)
				elif row[y] > (median + std) or row[y] < (median - std):
					temp_row.append(0)
				else:
					temp_row.append(row[y]+1)
			result.append(temp_row)
		return result

	def plot_histogram(self, values, bins):
		plt.clf()

		plt.plot(bins, values)

		plt.show()

	def fits_to_list(self, file_name):
		'''
		Open the fits file, select just the image data, and close the fits file.
		'''
		hdulist = fits.open(file_name)
		return hdulist[0].data
		hdulist.close()

	def run_analysis(self, img_in, img_out):
		'''
		This is where the code is actually run, so the total analysis
		package can be called from outside this file.
		'''
		img = self.fits_to_list(str(img_in))
		# Mask the image to remove high and low pixels, and any pixels out of FoV
		masked = self.masked_img2(img, 500)

		# Histogram of the maksed image, with any 0 pixels removed and matched sizes
		values, bins = self.pixel_value_list(masked)
		bins = np.delete(bins, len(bins)-1)
		bins = np.delete(bins, 0)
		values = np.delete(values, 0)
		self.plot_histogram(values, bins)

		# Output the masked image as a png
		self.array_to_png(str(img_out), masked)
		return "analysis complete"

	def array_to_png(self, file_path, pixel_grid):
		'''
		Recycled code from CSE 160 image homework
		to output a png image from an imput data array.
		'''

		size = len(pixel_grid[0]), len(pixel_grid)
		image = Image.new("L", size)

		print "Writing", size[0], 'x', size[1], "image to file", file_path

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

	print cg.run_analysis("20160221T205857_30.fits", "20160221T205857_30_analyzed.png")
