#! /usr/bin/python

"""
Cloud_Graph.py
Analyze and process images from the CloudCam. Applies masks, calculates
statistics, and outputs a .png image to analyzed/

All statistical information is saved in the FITS header,
and the FITS image is compressed.

TODO:
	Fix png naming to use a timestamp, not a chopped name

Dependencies:
	Run ./make to install all dependencies

Usage:
	Analyze all .fits images in images/:
		python Cloud_Graph.py
	Typically called from CloudCam.py

Output:
	Analyzed image, with histogram plot and statistics is
	output to analyzed as (Input_Name)_analyzed.png
"""

__author__ = ["J. Matt Armstrong"]
__copyright__ = "NA"
__credits__ = ["Joseph Huehnerhoff"]
__license__ = "GPL"
__version__ = "2.0"
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
from Cloud_Mask import CloudMask


class CloudGraph(object):
	def __init__(self):
		self.l = Logger() #Logger class creates logfile of processes
		self.dir = os.path.join(os.getcwd(),'logs')
		self.logType = 'cloud' # Parameter used in  Logger class to create logfile
		self.imglist = []
		self.count = 0
		self.cm = CloudMask()
		self.hdudata = None
		self.header = None

		# Memory locations for masks
		self.large_mask = None
		self.small_mask = None
		self.ne_mask = None
		self.n_mask = None
		self.nw_mask = None
		self.w_mask = None
		self.sw_mask = None
		self.s_mask = None
		self.se_mask = None
		self.e_mask = None


	def start_up_checks(self):
		"""
		Run once at start-up
		Checks for necessary folders and files
		Creates them if necessary
		"""

		# Produce any missing folders
		folder_list = ["gif", "logs", "images", "analyzed", "masks"]
		for folder in folder_list:
			if (os.path.isdir(folder)) == False:
				print "Creating directory "+str(folder)
				os.makedirs(folder)

		# Load masks into memory
		if os.path.isfile("masks/aperture_mask_500.npy") == True:
			print 'Loading mask files into memory.'
		else:
			print "Large aperture mask file not found, making one now."
			self.cm.make_aperture_mask(500)
			self.cm.make_aperture_mask(300)
			self.cm.make_wedge_mask(300)

		self.large_mask = np.load("masks/aperture_mask_500.npy")
		self.small_mask = np.load("masks/aperture_mask_300.npy")
		self.nw_mask = np.load("masks/1_wedge_mask.npy")
		self.w_mask = np.load("masks/2_wedge_mask.npy")
		self.sw_mask = np.load("masks/3_wedge_mask.npy")
		self.s_mask = np.load("masks/4_wedge_mask.npy")
		self.se_mask = np.load("masks/5_wedge_mask.npy")
		self.e_mask = np.load("masks/6_wedge_mask.npy")
		self.ne_mask = np.load("masks/7_wedge_mask.npy")
		self.n_mask = np.load("masks/8_wedge_mask.npy")

		return

	def dynamic_mask(self, image, maskname):
		"""
		Creates a numpy mask on the image, filtering out any
		pixel values that are negative or saturated

		Input:
			image			(Aperture masked numpy image)
		Output: Masked numpy array covering any pixels above or below the standard dev range
			masked1			(masked numpy array)
			median	*Float*	(median value of masked array)
			mean	*Float*	(mean value of masked array)
		"""

		# Make a masked array using the static mask and imput image
		pre_masked = ma.array(image, mask=maskname)

		# Mask saturated or empty
		masked1 = ma.masked_greater(pre_masked, 254)
		masked1 = ma.masked_less(masked1, 0)

		median = int(ma.median(masked1))
		mean = ma.mean(masked1)
		std = ma.std(masked1)

		mean = float('%.2f' % (mean))
		std = float('%.2f' % (std))
		
		print mean
		print std

		return masked1, median, mean, std

	def directional_statistics(self, image):
		# Compute directional statistics
		directions = ['NE', 'N', 'NW', 'W', 'SW', 'S', 'SE', 'E']
		dirdict = {'NE': self.ne_mask, 'N': self.n_mask, 'NW': self.nw_mask, 'W': self.w_mask, 'SW': self.sw_mask, 'S': self.s_mask, 'SE': self.se_mask, 'E': self.e_mask}
		for d in directions:
			print "Statistics for "+str(d)+" directional mask:"
			mask = dirdict[d]
			tmp_img, tmp_median, tmp_mean, tmp_std = self.dynamic_mask(image, mask)
			print "Median = "+str(tmp_median)
			print "Mean = "+str(tmp_mean)
			print "STD = "+str(tmp_std)
			self.header[str(d)+"_MED"] = tmp_median
			self.header[str(d)+"_STD"] = tmp_std
		return

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

		return result

	def scale_img(self, img, median, std):
		"""
		Scale the image based on the median and std
		Brings out cloud detail

		input:
			img			(masked numpy image to scale)\
			median		(median value of image)
			std			(std value of image)

		output:
			result		(scaled image)
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
			values 		(List of histogram counts)
			bins		(List of histogram bins)
			img_out		(Name of output image)
			masked 		(Masked numpy image)
			median		(Histogram median)
			mean		(Histogram mean)
			std			(Histogram standard dev)
			name		(Name of image)				[Replace with timestp]

		Output: png image file with the masked image, statistical and image information, and histogram plot
			Saves three copies of the image
				analyzed/img_out.png			(Archive storage location)
				gif/img_out.png					(Temp directory used to produce a gif)
				/var/www/html/latest.png		(Live view webpage displays this image)
			Every 10 images, produces a gif of the images in gif/
				/var/www/html/latest.png		(Live view webpage displays this gif)
		"""

		plt.clf()

		#Fill in the masked image for processing

		scaled_img = self.scale_img(masked, median, std)
		#img_masked, junk1, junk2, junk3 = self.dynamic_mask(masked, self.large_mask)
		img = Image.fromarray(scaled_img)

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

		img = img.rotate(90).resize((int(img.size[1]),int(img.size[0])), Image.ANTIALIAS)

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
		plt.draw()

		#Save the figure as a png
		gs.tight_layout(fig, h_pad=None)
		fig.savefig(img_out, cmap="grey", transparent=True, facecolor="black", edgecolor='none')

		fig.savefig(os.getcwd()+"/gif/gif"+str(self.count)+".png", cmap="grey", transparent=True, facecolor="black", edgecolor='none', clobber=True)

		"""
		#fig.savefig("/var/www/html/latest.png", cmap="grey", transparent=True, facecolor="black", edgecolor='none', clobber=True)
		"""
		#produce a gif of the last 10 images when self.count == 10
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
		self.hdudata, self.header = fits.getdata(file_name, header=True)
		return np.asarray(self.hdudata)

	def add_headers(self, expose, median, std, name, img_in):
		"""
		Add statistical and image information
		to the FITS header, close the FITS file,
		and zip the image to save space.

		Input:
			expose 		The length of the image exposure in seconds
			median		The statistical median of the image
			std			The statistical standard dev. of the image
			img_in		The name of the image

		Output:
			Saved and compressed FITS image
		"""
		# Add info to the FITS header
		self.header['IMG_NAME'] = name
		self.header['IMAGTYP'] = 'CloudCam'
		self.header['EXPTIME'] = float(expose)
		self.header['MEDIAN'] = median
		self.header['STD'] = std


		# Close and compress the FITS file, saving the header
		compressed = fits.CompImageHDU(self.hdudata, self.header, name=name)
		compressed.writeto(img_in, clobber=True)

		return

	def run_analysis(self, img_in, img_out, name, expose):
		"""
		This is where the code is actually run, so the total analysis
		package can be called from outside this file.

		Input: name of image in, name of image out, and chopped file name
		input:
			img_in			(name of input .fits image)
			img_out			(name of output png image)
			name 			(name file for timestamp)
		"""
		img = self.fits_to_list(str(img_in))
		print "Analyzing "+str(img_in)

		# Use small mask to calculate image statistics
		masked, median, mean, std = self.dynamic_mask(img, self.small_mask)
		print "Median = "+str(median)
		print "Mean = "+str(mean)
		print "Standard Dev = "+str(std)

		# Calculate directional statistics
		self.directional_statistics(masked)

		# Calculate histogram for small maksed image
		values, bins = self.pixel_value_list(masked)
		fixed_vals = np.append(values, 0)

		# Use large mask to produce image
		masked_img, junk1, junk2, junk3 = self.dynamic_mask(img, self.large_mask)

		# Produce output png with histogram info
		self.plot_histogram(fixed_vals, bins, img_out, masked_img, median, mean, std, name)

		# Add image data to the FITS header, compress the image
		self.add_headers(expose, median, std, name, img_in)

		# Log the activity
		self.l.logStr('Image\t%s,%s,%s,%s' % (str(img_out), str(median), str(mean), str(std)), self.logType)

		return median


if __name__=="__main__":
	"""
	Run terminal command in image directory(ls *.fits > image.txt)
	This will produce a text list of all fits files to process
	Run the program using a list of file names in a text file_path

	Log file will contain time stamp, img_name, median, mean, std
	"""

	location = os.getcwd()
	imagedir = os.path.join(location,'images/')


	cg = CloudGraph()
	cg.start_up_checks()
	
	# Produce a txt file with a list of .fits images in images/
	listdirect = os.path.join(os.getcwd(),'images/')
	imagelist = listdirect+'image.txt'
	print "Creating a list of fits files in images/"
	fitslist = []
	for fits in os.listdir(listdirect):
		if fits.endswith(".fits"):
			fitslist.append(fits)
	if len(fitslist) == 0:
		print "No FITS images found in images/"
		print "Ending Cloud_Graph.py"
		sys.exit()
	f = open(imagelist, "w")
	f.write("\n".join(map(lambda x: str(x), fitslist)))
	f.close()
	img_list = np.genfromtxt(imagelist, usecols = [0], unpack = True, dtype = 'str')

	for i in img_list:
		name = i.replace(".fits","")
		timestamp = name.split('_')
		try:
			expose = timestamp[1]
		except:
			expose = 'NA'
		if os.path.isfile(imagedir+name+".fits") == True:
			cg.run_analysis(imagedir+name+".fits", location+"/analyzed/"+name+'_analyzed.png', name, expose)
		else:
			print "File not found"
