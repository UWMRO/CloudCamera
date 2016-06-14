#! /usr/bin/python

"""
Cloud_Graph.py
Analyze and process images from the CloudCam. Applies masks, calculates
statistics, and outputs a .png image to analyzed/

TODO:
	Produce directional statistics
	Zip fits images after they are used

Dependencies:
	Run ./make to install all dependencies

Usage:
	Analyze all .fits images in images/:	python Cloud_Graph.py
	Typically called from CloudCam.py

Output:
	Analyzed image, with histogram plot and statistics is
	output to analyzed as (Input_Name)_analyzed.png
"""

__author__ = ["J. Matt Armstrong"]
__copyright__ = "NA"
__credits__ = ["Joseph Huehnerhoff"]
__license__ = "GPL"
__version__ = "1.5"
__maintainer__ = "J. Matt Armstrong"
__email__ = "jmarmstr@uw.edu"
__status__ = "Developement"

import numpy as np
import numpy.ma as ma
from astropy.io import fits
from scipy.misc import bytescale as Scale
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.figure import Figure
from matplotlib import gridspec
import matplotlib.ticker as mtick
import datetime
from logger import *
import os
from PIL import Image
import itertools
import sys
import subprocess
import shutil


class CloudGraph(object):
	def __init__(self):
		self.l = Logger() #Logger class creates logfile of processes
		self.dir = os.path.join(os.getcwd(),'logs')
		self.logType = 'cloud' # Parameter used in  Logger class to create logfile
		self.imglist = []
		self.count = 0
		self.static_mask = None
	def start_up_checks(self):
		"""
		Run once at start-up
		Checks for necessary folders and files
		Creates them if necessary

		Returns:
			img_list			(list of .fits in images/)
			self.static_mask	(circular aperture mask loaded into memory)
		"""

		# Load mask into memory
		if os.path.isfile("static_mask.npy") == True:
			print 'Loading static mask file.'
		else:
			print "Static mask file not found, making one now."
			print self.make_static_mask(500)
		self.static_mask = np.load("static_mask.npy")

		# Produce any missing folders
		folder_list = ["gif", "logs", "images", "analyzed"]
		for folder in folder_list:
			if (os.path.isdir(folder)) == False:
				print "Creating directory "+str(folder)
				os.makedirs(folder)

		# Produce a txt file with a list of .fits images in images/
		listdirect = os.path.join(os.getcwd(),'images/')
		imagelist = listdirect+'image.txt'
		print "Creating a list of fits files in images/"
		fitslist = []
		for fits in os.listdir(listdirect):
			if fits.endswith(".fits"):
				fitslist.append(fits)
		f = open(imagelist, "w")
		f.write("\n".join(map(lambda x: str(x), fitslist)))
		f.close()
		img_list = np.genfromtxt(imagelist, usecols = [0], unpack = True, dtype = 'str')

		return img_list, self.static_mask


	def make_static_mask(self, radius):
		"""
		Used to make a static aperture mask, which can be
		multiplied by the analysis image to remove any pixels
		outside the radius from the center.

		Input: Radius to mask from center of image
		Output: Aperture asked numpy array the same size as the image.
		"""
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
		"""
		Creates a numpy mask on the image, filtering out any
		pixel values that are more than sigrange*std from the median value

		Input: numpy array of the image, sigrange for multiplier on standard dev range
		Output: Masked numpy array covering any pixels above or below the standard dev range
		"""

		# Make a masked array using the static mask and imput image
		pre_masked = ma.array(image, mask=self.static_mask)

		# Mask saturated or empty
		masked1 = ma.masked_greater(pre_masked, 254)
		masked1 = ma.masked_less(masked1, 0)

		median = ma.median(masked1)
		mean = ma.mean(masked1)
		std = ma.std(masked1)

		return masked1, median, mean, std


	def pixel_value_list(self, image):
		"""
		Produce two arrays, the first is a list of the binned pixel values
		and the second is the number of pixels at that value

		Input: masked numpy array of the image
		Output: Two lists of histogram data on the image. ([bins],[values])
		"""

		# Compress the array into a list of pixel values
		compressed = ma.compressed(image)

		# Find highest pixel value
		max_val = np.amax(compressed)

		# Make a histogram of the compressed list
		result = np.histogram(compressed, bins=max_val, normed=True)
		#print result[0]
		#print result[1]
		return result

	def scale_img(self, img, median, std):
		"""
		Scale the image based on the median and std
		Brings out cloud detail
		"""

		masked_img = img.filled(fill_value = 0)

		bytehigh = int((median + std))
		if bytehigh > 255:
			bytescale = 255

		#bytelow = int((median - std))
		#if bytelow < 0:
		bytelow = 0

		result = Scale(masked_img.astype(float), cmax = bytehigh, cmin = bytelow) #, high = bytehigh, low = bytelow)
		return result

	def plot_histogram(self, values, bins, img_out, masked, median, mean, std, name):
		"""
		Statistical plotting and output function.

		Input: Value list, Bin list, Name of output, Masked image, median value, mean value, standard dev, image name
		Output: png image file with the masked image, statistical and image information, and histogram plot
		"""

		plt.clf()

		#Fill in the masked image for processing

		scaled_img = self.scale_img(masked, median, std)
		img_masked, junk1, junk2, junk3 = self.dynamic_mask(scaled_img, 3)
		img = Image.fromarray(img_masked)


		#Set up plotting environment
		fig, ax = plt.subplots(2,1)
		fig.set_size_inches(8,11)       # width, height
		fig.tight_layout()
		gs = gridspec.GridSpec(2,1,height_ratios=[4,1], wspace=0.0, hspace=0.0)

		#Find timestamp, change this to use header info instead
		timestamp = name.split('_')
		try:
			timetest = timestamp[1]
		except:
			timetest = 'NA'

		#Plot the masked image, allow for arbitrary rotation
		ax0 = plt.subplot(gs[0])
		ax0.axis('off')

		img = img.rotate(90).resize((int(img.size[0]),int(img.size[1])), Image.ANTIALIAS)

		# Insert statistical information into the image
		ax0.text(0, 1240, name[0:4]+'-'+name[4:6]+'-'+name[6:8]+'   '+name[9:11]+':'+name[11:13]+':'+name[13:15], size = 16, color="white", horizontalalignment='left')
		ax0.text(0, 1280, 'Exposure = '+str(timetest)+' [s]', size = 16, color="white", horizontalalignment='left', )
		ax0.text(1100, 1200 , 'Median = %.1f' % (median), size = 16, color="white", horizontalalignment='right')
		ax0.text(1100, 1240, "Mean = %.2f" % (mean), size = 16, color="white", horizontalalignment='right')
		ax0.text(1100, 1280, 'Standard Dev = %.2f' % (std), size = 16, color="white", horizontalalignment='right')
		ax0.imshow(img, cmap="gray")

		#Plot the histogram
		ax1 = plt.subplot(gs[1])
		ax1.bar(bins, (values*100.0), alpha=1.0)
		ax1.set_xlim([int(median-3*std),int(median+3*std)])
		ax1.set_xlabel('Pixel Value', size=16)
		ax1.xaxis.label.set_color('white')
		plt.locator_params(axis='y',nbins=6)
		ax1.tick_params(axis='x', colors='white', labelsize=12)
		#ax1.yaxis().set_visible(False)
		plt.draw()

		#Save the figure as a png
		gs.tight_layout(fig, h_pad=None)
		fig.savefig(img_out, cmap="grey", transparent=True, facecolor="black", edgecolor='none')

                fig.savefig(os.getcwd()+"/gif/gif"+str(self.count)+".png", cmap="grey", transparent=True, facecolor="black", edgecolor='none', clobber=True)

		fig.savefig("/var/www/html/latest.png", cmap="grey", transparent=True, facecolor="black", edgecolor='none', clobber=True)

		self.count += 1
		if self.count == 10:
			print "Producing gif image"
			command = "sudo convert -delay 40 -loop 0 "+os.getcwd()+"/gif/*.png /var/www/html/latest.gif"
			out = subprocess.Popen(command, stdout = subprocess.PIPE, shell=True)
			self.count = 0
			self.imglist = []
			time.sleep(15)
			shutil.rmtree(os.getcwd()+"/gif")
			os.makedirs(os.getcwd()+"/gif")
		plt.close("all")
		return

	def fits_to_list(self, file_name):
		"""
		Try to open the fits file.
		If the file doesn't exist, say so and return.
		Otherwise, select just the image data as a numpy array
		and close the fits file.

		Input: File name
		Output: Numpy array of image data
		"""
		hdulist = fits.open(file_name)
		return np.asarray(hdulist[0].data)
		hdulist.close()

	def run_analysis(self, img_in, img_out, name):
		"""
		This is where the code is actually run, so the total analysis
		package can be called from outside this file.

		Input: name of image in, name of image out, and chopped file name
		"""
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

		return median


if __name__=="__main__":
	"""
	Run terminal command in image directory(ls *.fits > image.txt)
	This will produce a text list of all fits files to process
	Run the program using a list of file names in a text file_path

	Change the directory for images and create a folder inside
	/analyzed

	Log file will contain time stamp, img_name, median, mean, std
	"""

	location = os.getcwd()
	imagedir = os.path.join(location,'images/')


	cg = CloudGraph()
	img_list, static_mask = cg.start_up_checks()


	for i in img_list:
		name = i.replace(".fits","")
		if os.path.isfile(imagedir+name+".fits") == True:
			print cg.run_analysis(imagedir+name+".fits", location+"/analyzed/"+name+'_analyzed.png', name)
		else:
			print "File not found"
