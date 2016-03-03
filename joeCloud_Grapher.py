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

	def pixel_value_list(self, image):
		'''
		Produce two arrays, the first is a list of the pixel values
		and the second is the number of pixels at that value
		'''
		#Trying to use numpy histogram to improve processing speed.
		result = np.histogram(image, bins = np.arange(np.amax(image)+1), normed = True)
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
		result = np.empty([1024])
		std = 3*(np.std(image))
		median = np.median(image)
		mean = np.mean(image)
		#result = ma.masked_less(image,float(80)).filled(0)

		print image

		"""for x in range(len(image)):
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
		result = np.asarray(result)  #==> make numpyish again, you should probably just preserve numpy array types in your for loop"""
		print image.size
		for x in range(len(image)):
                        shift_x = x-(1024/2)
                        for y in range(len(image[x])):
                                row = image[x]
                                shift_y = y-(1280/2)
                                if np.sqrt((shift_x)**2 + (shift_y)**2) > radius:
                                        image[x][y]=0
                                elif row[y] > (median + std) or row[y] < (median - std):
                                        image[x][y]=0
                                #else:
                                #        image[row[y]+1)
                        #np.append(result,temp_row)
		print image.size
		return image, median, mean, std


	def plot_histogram(self, values, bins, img_out, masked, median, mean, std):
		plt.clf()

		fig = plt.figure()

		#plt.subplot(2,1,1)

		plt.gray()
		plt.axis('off')

		img = Image.fromarray(masked)
		img = img.rotate(90).resize((int(img.size[1]*.55),int(img.size[0]*.55)), Image.ANTIALIAS)
		fig.figimage(img, 100, -50)

		#plt.subplot(3,1,3)
		#==> you could remove your histogram function and incorporate it all into plt.hist, but this is also ok
		print len(bins), len(values)

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
		#plt.show()


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
		l = Logger()
		img = self.fits_to_list(str(img_in))
		print "Analyzing "+str(img_in)
		# Mask the image to remove high and low pixels, and any pixels out of FoV
		masked, median, mean, std = self.masked_img2(img, 500)
		print "Median = "+str(median)
		print "Mean = "+str(mean)
		print "Standard Dev = "+str(std)

		# Histogram of the maksed image, with any 0 pixels removed and matched sizes
		values, bins = self.pixel_value_list(masked)
		bins =	np.delete(bins,0)
		values[0] = 0
		print values, bins
		self.plot_histogram(values, bins, img_out, masked, median, mean, std)

		# Output the masked image as a png
		#self.array_to_png(str(img_out), masked)
		l.logStr('Image\t%s,%s,%s,%s' % (str(img_out), str(median), str(mean), str(std)), self.logType)
		return "analysis complete"

	"""
	Currently not used

	def array_to_png(self, file_path, pixel_grid):
		'''
		#Recycled code from CSE 160 image homework
		#to output a png image from an imput data array.
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
	"""

if __name__=="__main__":
	'''
	Run the program using a list of file names in a text file_path
	one line for each file_path
	Change the directory for images and create a folder inside
	/analyzed

	Log file will go to a /logs folder from this program's directory
	img_name, median, mean, std

	'''
	cg = CloudGraph()
	#dir = '/home/matt/College/AUEG/CloudCamera-master/Images/'
	"""dir = os.getcwd()
	img_list = np.genfromtxt(dir+'nightlist.txt', usecols = [0], unpack = True, dtype = 'str')
	for i in img_list:
		name = i.replace(".fits","")
		print cg.run_analysis(dir+name+".fits", dir+"analyzed/"+name+'_analyzed.png')"""
	img = "20160221T205857_30"
	print cg.run_analysis(img+".fits", img+"_analyzed.png")
