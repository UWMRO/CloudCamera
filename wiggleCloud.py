#! /usr/bin/python
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

"""
wiggleCloud.py
Produces movie images in mp4 format

TODO:


Usage:
"""

__author__ = ["J. Matt Armstrong"]
__copyright__ = "NA"
__credits__ = ["Joseph Huehnerhoff"]
__license__ = "GPL"
__version__ = "2.0"
__maintainer__ = "J. Matt Armstrong"
__email__ = "jmarmstr@uw.edu"
__status__ = "Developement"

import os
import subprocess
import time
import shutil
from transfer import transfer
import threading
from PIL import Image
import numpy as np
import datetime
import traceback

class CloudGif(object):
	def __init__(self):
		self.trans = transfer()
		self.host = 'galileo.apo.nmsu.edu'
                self.user = 'jwhueh'
                self.serverDir = 'public_html/CloudCamera/'


	def cleanDir(self, dir = None):
		list = sorted(os.listdir(os.path.join(os.getcwd(),dir)))
		for img in list:
			if img.endswith(".png"):
				print (img)
				t1 = img.split('_')
				t1_split = datetime.datetime.strptime(t1[0], "%Y%m%dT%H%M%S")
				t2 = datetime.datetime.now()
				diff =  t2 - t1_split
				if diff > datetime.timedelta(minutes=60):
					os.remove(os.path.join(os.getcwd(), dir, img))
					print ('removing: ',img, diff)
	
	def hourWiggle(self, dir=None):
		self.cleanDir(dir)
		if dir == "gif":
			gifName = 'latest.mp4'
			gifPath = os.path.join(os.getcwd(), dir, gifName)
                if dir == "gif_map":
                        gifName = 'latest_map.mp4'
			gifPath = os.path.join(os.getcwd(), dir, gifName)
		print ("Producing gif image")
		if os.path.isfile(gifPath):
			os.remove(gifPath)
	
		command = "nice -5 ffmpeg -y -f image2 -r 6 -pattern_type glob -i 'gif/*.png' " + str(gifName)
		out = subprocess.Popen(command, stdout = subprocess.PIPE, shell=True)
		stdoutp, stderrp = out.communicate()
		print (stdoutp)
		if os.path.isfile(gifName):
			print ("gif image produced")
			shutil.copyfile(gifName, os.path.join("/var/www/html/", gifName))
			self.trans.uploadFile(self.host, self.user, gifName, self.serverDir)
		else:
			print ("gif was not created")
		return

	def dayWiggle(self):
		dayName = time.strftime("%Y%m%d")
                gifPath = os.path.join('/raid/CloudCamera/', dayName)
		command = "ffmpeg -y -f image2 -r 6 -pattern_type glob -i '%s/*.png' %s" % (str(gifPath),str(dayName+'.mp4'))
		self.trans.remoteCommand('analysis', 'jwhueh', command)
                return


if __name__ ==  "__main__":
	cg = CloudGif()
	x = 0	
	while True:
		cg.hourWiggle('gif')
		x = x+1
		if x == 20:
			print ('making long term gif')
			cg.dayWiggle()
			x = 0
		time.sleep(180)
		
