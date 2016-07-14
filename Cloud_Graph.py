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
from astropy.io import fits as Fits
import scipy.ndimage
from scipy.misc import bytescale as Scale
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.figure import Figure
from matplotlib import gridspec
import matplotlib.ticker as mtick
import datetime
from logger import *
import os
from PIL import Image
from PIL import ImageOps
import itertools
import sys
import subprocess
import shutil
from Cloud_Mask import CloudMask
from transfer import transfer
from shutil import copyfile
from CloudParams import *

class CloudGraph(object):
	def __init__(self):
		self.l = Logger() #Logger class creates logfile of processes
		self.dir = os.path.join(os.getcwd(),'logs')
		self.logType = 'cloud' # Parameter used in  Logger class to create logfile
		self.imglist = []
		self.dir_stats = {}
		self.count = 0
		self.cm = CloudMask()
		self.hdudata = None
		self.header = None
		self.scaleimg = scale_img
		self.bin_eros = binary_erosion
		self.trans = transfer()
		self.rotate = rotate

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

	def run_analysis(self, img_in, img_out, name, expose, gain):
		"""
		This is where the code is actually run, so the total analysis
		package can be called from outside this file.

		Input: name of image in, name of image out, and chopped file name
		input:
			img_in			(name of input .fits image)
			img_out			(name of output png image)
			name 			(name file for timestamp)
		"""
		img = self.fits_to_list(img_in)
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
		self.plot_histogram(fixed_vals, bins, img_out, masked_img, median, mean, std, name, gain)

		# Add image data to the FITS header, compress the image
		self.add_headers(expose, median, std, name, img_in)

		# Log the activity
		self.l.logStr('Image\t%s,%s,%s,%s' % (str(img_out), str(median), str(mean), str(std)), self.logType)

		return median

	def fits_to_list(self, file_name):
		"""
		Try to open the fits file.
		If the file doesn't exist, say so and return.
		Otherwise, select just the image data as a numpy array
		and close the fits file.

		Input: File name
		Output: Numpy array of image data
		"""
		#fits.open(file_name, mode='w')
		self.hdudata, self.header = Fits.getdata(file_name, header=True)
		return np.asarray(self.hdudata)

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
			self.dir_stats[d] = {'Median':tmp_median, 'Mean':tmp_mean, 'STD':tmp_std}
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

		bytehigh = int(median + (2*std))
		if bytehigh > 255:
			bytescale = 255

		bytelow = int(median - (2*std))
		if bytelow < 0:
			bytelow = 0

		result = Scale(img.astype(float), cmax = bytehigh, cmin = bytelow) #, high = bytehigh, low = bytelow)
		return result

	def plot_histogram(self, values, bins, img_out, masked, median, mean, std, name, gain):
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
		masked_img = masked.filled(fill_value = 0)

		if self.scaleimg == True:
			scaled_img = self.scale_img(masked_img, median, std)
			img = Image.fromarray(scaled_img)
		else:
			img = Image.fromarray(masked_img)

		#Set up plotting environment
		fig, ax = plt.subplots(2,2)
		fig.set_size_inches(10,10)       # width, height
		fig.tight_layout()
		gs = gridspec.GridSpec(10,10)		# height, width

		#Find timestamp, change this to use header info instead
		timestamp = name.split('_')
		try:
			exp = timestamp[1]
		except:
			exp = 'NA'

		#Plot the masked image, allow for arbitrary rotation
		ax[0,0] = plt.subplot(gs[:7,:7])
		ax[0,0].axis('off')

		img = img.rotate(self.rotate).resize((1280,1024), Image.ANTIALIAS)
		img = ImageOps.mirror(img)		
		img = scipy.ndimage.median_filter(img, 3)
		#img = scipy.ndimage.gaussian_filter(img, sigma=3)

		#Use binary erosion to smooth the image
		if self.bin_eros == True:
			img = scipy.ndimage.morphology.binary_erosion(img)

		scipy.misc.imsave('latestimg.png', img)
		shutil.copyfile("latestimg.png", "/var/www/html/latestimg.png")

  #try:
                self.trans.openConnection()
                f_out = ["latestimg.png"]
                for f in f_out:
                        if os.path.isfile(f):
                                print 'uploading',str(f)
                                self.trans.uploadFile(f)
                self.trans.closeConnection()
                #except:
                #       print "could not connected to remote server"
                


		# Insert statistical information into the image
		ax[0,0].text(0, 1200, name[0:4]+'-'+name[4:6]+'-'+name[6:8]+'   '+name[9:11]+':'+name[11:13]+':'+name[13:15], size = 16, color="white", horizontalalignment='left')
		ax[0,0].text(0, 1260, 'Exposure = '+str(exp)+' [s]', size = 16, color="white", horizontalalignment='left', )
		ax[0,0].text(0, 1320, 'Gain = '+str(gain), size = 16, color = "white", horizontalalignment = "left")
		ax[0,0].text(1200, 1200 , 'Median = %.1f' % (median), size = 16, color="white", horizontalalignment='right')
		ax[0,0].text(1200, 1260, "Mean = %.2f" % (mean), size = 16, color="white", horizontalalignment='right')
		ax[0,0].text(1200, 1320, 'Standard Dev = %.2f' % (std), size = 16, color="white", horizontalalignment='right')
		ax[0,0].imshow(img, cmap="gray")

		#Plot the histogram
		ax[1,0] = plt.subplot(gs[8:9,:10])
		ax[1,0].bar(bins, (values*100.0), alpha=1.0)
		ax[1,0].set_xlim(0,255)
		ax[1,0].set_xlabel('Pixel Value', size=16)
		ax[1,0].xaxis.label.set_color('white')
		plt.locator_params(axis='y',nbins=6)
		ax[1,0].tick_params(axis='x', colors='white', labelsize=12)

		#Plot directional Median values
		ax[0,1] = plt.subplot(gs[1:4,7:])
		sizes = [1,1,1,1,1,1,1,1]
		med_data = []
		for key in self.dir_stats:
			tmp_med = self.dir_stats[key]['Median']
			#normalize to max pixel value
			norm_tmp_med = tmp_med / 255.0
			med_data.append(norm_tmp_med)
		cmap = plt.cm.gray
		colors = cmap(med_data)
		ax[0,1].pie(sizes, colors=colors)
		#ax[0,1].subtitle('Median', color="white")

		#Plot directional Median values
		ax[1,1] = plt.subplot(gs[4:7,7:])
		sizes = [1,1,1,1,1,1,1,1]
		std_data = []
		for key in self.dir_stats:
			tmp_std = self.dir_stats[key]['STD']
			#normalize to 100 std
			if tmp_std <= 50:
				tmp_std = tmp_std / 50
			else:
				tmp_std = 1.0
			std_data.append(tmp_std)
		cmap = plt.cm.gray
		colors = cmap(std_data)
		ax[1,1].pie(sizes, colors=colors)
		ax[1,1].text(100, 100, 'STD', size=12, color="white")
		
		plt.draw()

		#Save the figure as a png
		
		fig.savefig(img_out, cmap="grey", transparent=True, facecolor="black", edgecolor='none')

		fig.savefig(os.getcwd()+"/gif/gif"+str(self.count)+".png", cmap="grey", transparent=True, facecolor="black", edgecolor='none', clobber=True)

		fig.savefig("latest.png", cmap="grey", transparent=True, facecolor="black", edgecolor='none', clobber=True)
		shutil.copyfile("latest.png", "/var/www/html/latest.png")
		
		#send the latest image to galileo
		#try:
		self.trans.openConnection()
		f_out = ["latest.png"]
		for f in f_out:
			if os.path.isfile(f):
				print 'uploading',str(f)
				self.trans.uploadFile(f)
		self.trans.closeConnection()
		#except:
		#	print "could not connected to remote server"
		

		#produce a gif of the last 10 images when self.count == 10
		self.count += 1
		if self.count == 10:
			print "Producing gif image"
			command = "convert -delay 40 -loop 0 "+os.getcwd()+"/gif/*.png latest.gif"
			out = subprocess.Popen(command, stdout = subprocess.PIPE, shell=True)
			self.count = 0
			self.imglist = []
			time.sleep(15)
			shutil.rmtree(os.getcwd()+"/gif")
			os.makedirs(os.getcwd()+"/gif")
			time.sleep(8)
			# Send the gif to Galileo
			shutil.copyfile("latest.gif", "/var/www/html/latest.gif")
			self.trans.openConnection()
			print("uploading latest.gif")
			self.trans.uploadFile("latest.gif")
			self.trans.closeConnection()
		plt.close("all")
		return

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
		compressed = Fits.CompImageHDU(self.hdudata, self.header, name=name)
		compressed.writeto(img_in, clobber=True)

		return


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
