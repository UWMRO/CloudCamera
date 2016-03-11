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
from matplotlib import gridspec
import datetime
from logger import *
import os
from PIL import Image
import itertools
import sys



class CloudGraph(object):
	def __init__(self):
		self.l = Logger() #Logger class creates logfile of processes
		self.dir = os.path.join(os.getcwd(),'logs')
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
		pixel values that are more than sigrange*std from the median value
		'''

		# Make a masked array using the static mask and imput image
		pre_masked = ma.array(image, mask=static_mask)

		# Statictics on the masked image
		std = (np.std(pre_masked))
		median = ma.median(pre_masked)
		mean = ma.mean(pre_masked)

		# Mask any pixels above or below the std from median
		stdrange = sigrange*std
		result1 = ma.masked_greater(pre_masked, (median+stdrange))
		result = ma.masked_less(result1, (median-stdrange))

		return result, median, mean, std


	def pixel_value_list(self, image):
		'''
		Produce two arrays, the first is a list of the pixel values
		and the second is the number of pixels at that value
		'''

		# Compress the array into a list of pixel values
		compressed = image.compressed()

		# Find highest pixel value
		max_val = np.amax(compressed)

		# Make a histogram of the compressed list
		result = np.histogram(compressed, bins=max_val, normed=True)
		return result

	def plot_histogram(self, values, bins, img_out, masked, median, mean, std, name):
		plt.clf()
		masked_img = ma.filled(masked, 0)
		img = Image.fromarray(masked_img)

		fig, ax = plt.subplots(2,1)
		fig.set_size_inches(8,11)       # width, height
		fig.tight_layout()
		gs = gridspec.GridSpec(2,1,height_ratios=[4,1], wspace=0.0, hspace=0.0)

		timestamp = name.split('_')
		try:
			timetest = timestamp[1]
		except:
			timetest = 'NA'


		ax0 = plt.subplot(gs[0])
		ax0.axis('off')
		img = img.rotate(90).resize((int(img.size[1]),int(img.size[0])), Image.ANTIALIAS)

		ax0.text(0, 1240, name[0:4]+'-'+name[4:6]+'-'+name[6:8]+'   '+name[9:11]+':'+name[11:13]+':'+name[13:15], size = 16, color="white", horizontalalignment='left')
		ax0.text(0, 1280, 'Exposure = '+str(timetest)+' [s]', size = 16, color="white", horizontalalignment='left', )
		ax0.text(1100, 1200 , 'Median = %.1f' % (median), size = 16, color="white", horizontalalignment='right')
		ax0.text(1100, 1240, "Mean = %.2f" % (mean), size = 16, color="white", horizontalalignment='right')
		ax0.text(1100, 1280, 'Standard Dev = %.2f' % (std), size = 16, color="white", horizontalalignment='right')
		ax0.imshow(img, cmap="gray")

		ax1 = plt.subplot(gs[1])
		ax1.bar(bins, (values*100.0), alpha=1.0)
		ax1.set_ylabel('% pixels', size=16)
		ax1.set_xlabel('Pixel Value', size=16)
		ax1.yaxis.label.set_color('white')
		ax1.xaxis.label.set_color('white')
		ax1.yaxis.set_label_position("right")
		ax1.yaxis.tick_right()
		plt.yticks(np.arange(0,(np.max(values*100))))
		ax1.tick_params(axis='x', colors='white', labelsize=16)
		ax1.tick_params(axis='y', colors='white', labelsize=16)
		plt.draw()

		gs.tight_layout(fig, h_pad=None)
		fig.savefig(img_out, cmap="grey", transparent=True, facecolor="black", edgecolor='none')
		plt.close("all")
		return

	def fits_to_list(self, file_name):
		'''
		Try to open the fits file.
		If the file doesn't exist, say so and return.
		Otherwise, select just the image data as a numpy array
		and close the fits file.
		'''
		hdulist = fits.open(file_name)
		return np.asarray(hdulist[0].data)
		hdulist.close()

	def run_analysis(self, img_in, img_out, name):
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

		# Histogram of the maksed image, with matched sizes
		values, bins = self.pixel_value_list(masked)
		fixed_vals = np.append(values, 0)
		self.plot_histogram(fixed_vals, bins, img_out, masked, median, mean, std, name)

		# Log the activity
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

	if os.path.isfile("static_mask.npy") == True:
		print 'Loading static mask file.'
		static_mask = np.load("static_mask.npy")
	else:
		print "Static mask file not found, making one now."
		print cg.make_static_mask(500)
		static_mask = np.load("static_mask.npy")

	'''
	test_img = "20160221T205857_30"
	print cg.run_analysis(test_img+".fits", test_img+'_analyzed.png', test_img)

	'''
	img_list = np.genfromtxt(list, usecols = [0], unpack = True, dtype = 'str')

	for i in img_list:
		name = i.replace(".fits","")
		if os.path.isfile(dir+name+".fits") == True:
			name = name.replace("bias_","")
			print cg.run_analysis(dir+name+".fits", dir+"analyzed/"+name+'_analyzed.png', name)
		else:
			print "File not found"
