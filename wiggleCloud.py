#! /usr/bin/python

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

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
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
				t1 = img.split('_')
				t1_split = datetime.datetime.strptime(t1[0], "%Y%m%dT%H%M%S")
				t2 = datetime.datetime.now()
				diff =  t2 - t1_split
				if diff > datetime.timedelta(minutes=60):
					os.remove(os.path.join(os.getcwd(), dir, img))
					print ('removing: ',img, diff)
	
	def make_gif(self, dir=None):
		if dir == "gif":
			gifName = 'latest.mp4'
			gifPath = os.path.join(os.getcwd(), dir, gifName)
                if dir == "gif_map":
                        gifName = 'latest_map.gif'
			gifPath = os.path.join(os.getcwd(), dir, gifName)
		print "Producing gif image"
		if os.path.isfile(gifPath):
			os.remove(gifPath)
	
		#command = "nice -5 convert -limit memory 500M -delay 40 -loop 0 "+os.getcwd()+"/"+dir+"/*.png " + gifName
		command = "nice -5 ffmpeg -y -f image2 -r 6 -pattern_type glob -i 'gif/*.png' " + str(gifName)
		print command
		out = subprocess.Popen(command, stdout = subprocess.PIPE, shell=True)
		stdoutp, stderrp = out.communicate()
		print stdoutp
		if os.path.isfile(gifName):
			print "gif image produced"
			shutil.copyfile(gifName, os.path.join("/var/www/html/", gifName))
			self.trans.uploadFile(self.host, self.user, gifName, self.serverDir)
		else:
			print "gif was not created"
		return


if __name__ ==  "__main__":
	cg = CloudGif()
	
	while True:
		subDir = 'gif'
		cg.cleanDir(subDir)
		cg.make_gif(180, subDir)
		time.sleep(180)
