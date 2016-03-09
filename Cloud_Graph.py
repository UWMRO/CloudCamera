'''
Test code for Cloud Camera histogram plotting
Used to determine the mean value of each row in an image
to be used for later analysis
'''

__author__ = "J. Matt Armstrong"
__copyright__ = "NA"
__credits__ = ["Nathen Nguyen", "Joseph Huehnerhoff"]
__license__ = "GPL"
__version__ = "0.3"
__maintainer__ = "J. Matt Armstrong"
__email__ = "jmarmstr@uw.edu"
__status__ = "Developement"

import numpy as np
import numpy.ma as ma
from astropy.io import fits
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.figure import Figure
import time
from logger import *
import os
from PIL import Image
import itertools
import sys



class CloudGraph(object):
	def __init__(self):
		self.l = Logger() #Logger class creates logfile of processes
		self.dir = str(dir)+"/logs"
		self.logType = 'cloud' # Parameter used in  Logger class to create logfile

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

	def make_static_mask(self, radius):
		'''
		Used to make a static aperture mask, which can be
		multiplied by the analysis image to remove any pixels
		outside the radius from the center.
		'''
		result = []

		for x in range(1024):
			shift_x = x-(1024/2)
			temp_row = []
			for y in range(1280):
				shift_y = y-(1280/2)
				if np.sqrt((shift_x)**2 + (shift_y)**2) > radius:
					temp_row.append(1)
				else:
					temp_row.append(0)
			result.append(temp_row)
		np.save("static_mask", np.asarray(result))
		return "Static mask saved"

	def dynamic_mask(self, image, sigrange):
		'''
		Creates a numpy mask on the image, filtering out any
		pixel values that are more than range*std from the median value
		'''
		pre_masked = ma.array(image, mask=static_mask)

		std = sigrange*(np.std(pre_masked))
		median = ma.median(pre_masked)
		mean = ma.mean(pre_masked)

		result1 = ma.masked_greater(pre_masked, (median+std))
		result = ma.masked_less(result1, (median-std))

		return result, median, mean, std


	def pixel_value_list(self, image):
		'''
		Produce two arrays, the first is a list of the pixel values
		and the second is the number of pixels at that value
		'''
		#Trying to use numpy histogram to improve processing speed.

		compressed = image.compressed()

		max_val = np.amax(compressed)

		result = np.histogram(compressed, bins=max_val)
		return result

	def plot_histogram(self, values, bins, img_out, masked, median, mean, std):
		plt.clf()

		fig = plt.figure()

		#plt.subplot(2,1,1)

		plt.gray()
		plt.axis('off')

		masked_img = ma.filled(masked, 0)

		img = Image.fromarray(masked_img)
		img = img.rotate(90).resize((int(img.size[1]*.55),int(img.size[0]*.55)), Image.ANTIALIAS)
		fig.figimage(img, 100, -50)

		#plt.subplot(3,1,3)
		#==> you could remove your histogram function and incorporate it all into plt.hist, but this is also ok


		ax = plt.axes([.2,.05,.6,.2,]) #[xstart,ystart, xfinal,yfinal]
		ax.bar(bins, values, alpha=.4)

		ax.yaxis.label.set_color('white')
		ax.xaxis.label.set_color('white')

		plt.ylabel('% pixels', size=8)
		plt.xlabel('Pixel Value', size=8)
		ax.tick_params(axis='x', colors='white', labelsize=8)
		ax.tick_params(axis='y', colors='white', labelsize=8)
		plt.draw()

		max_val = np.max(values)

		plt.text(60, max_val - .005 , 'Median = %.1f' % (median), size = 8, color="white")
		plt.text(60, max_val - 0.009, "Mean = %.2f" % (mean), size = 8, color="white")
		plt.text(60, max_val - 0.013, 'Standard Dev = %.2f' % (std), size = 8, color="white")

		plt.savefig(img_out, transparent=True)

	def fits_to_list(self, file_name):
		'''
		Open the fits file, select just the image data, and close the fits file.
		'''
		hdulist = fits.open(file_name)
		return np.asarray(hdulist[0].data)
		hdulist.close()

	def run_analysis(self, img_in, img_out):
		'''
		This is where the code is actually run, so the total analysis
		package can be called from outside this file.
		'''
		img = self.fits_to_list(str(img_in))
		print "Analyzing "+str(img_in)
		# Mask the image to remove high and low pixels, and any pixels out of FoV
		masked, median, mean, std = self.dynamic_mask(img, 3)
		print "Median = "+str(median)
		print "Mean = "+str(mean)
		print "Standard Dev = "+str(std)

		# Histogram of the maksed image, with any 0 pixels removed and matched sizes
		values, bins = self.pixel_value_list(masked)
		fixed_vals = np.append(values, 0)
		self.plot_histogram(fixed_vals, bins, img_out, masked, median, mean, std)

		# Output the masked image as a png
		#self.array_to_png(str(img_out), masked)
		self.l.logStr('Image\t%s,%s,%s,%s' % (str(img_out), str(median), str(mean), str(std)), self.logType)
		return "Analysis complete"


if __name__=="__main__":
	'''
	Run the program using a list of file names in a text file_path
	one line for each file_path
	change the image list file name

	Change the directory for images and create a folder inside
	/analyzed

	Log file will go to a /logs folder from this program's directory
	img_name, median, mean, std

	'''
	cg = CloudGraph()
	dir = '/home/matt/College/AUEG/CloudCamera-master/Images/'
	list = dir+'image.txt'

	# Make a new static mask file
	# print cg.make_static_mask(500)

	static_mask = np.load("static_mask.npy")
	'''
	img_list = np.genfromtxt(list, usecols = [0], unpack = True, dtype = 'str')
	for i in img_list:
		name = i.replace(".fits","")
		print cg.run_analysis(dir+name+".fits", dir+"analyzed/"+name+'_analyzed.png')

	'''
	img = "20160221T205857_30"
	print cg.run_analysis(img+".fits", img+"_analyzed.png")
