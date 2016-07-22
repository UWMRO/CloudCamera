'''
CloudCam gif production routine
'''
import os
import subprocess
import time
import shutil
from transfer import transfer
import threading
from PIL import Image
from images2gif import writeGif
import numpy as np
import datetime
import traceback

class CloudGif(object):
	def __init__(self):
		self.trans = transfer()

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
					print 'removing: ',img, diff
	
	def findImg(self, dir = None):
	       	listdirect = os.path.join(os.getcwd(),dir)
	        
        	print "Creating a list of png files in "+str(dir)
        	imglist = []
        	for img in os.listdir(listdirect):
                	if img.endswith(".png"):
                        	img = dir+"/"+img
                        	imglist.append(img)
        	if len(imglist) == 0:
                	print "No images found in "+str(dir)
                	print "Ending Cloud_gif.py"
			return
        	
        	#img_list = np.genfromtxt(imagelist, usecols = [0], unpack = True, dtype = 'str')
        	print "gif list has "+str(len(imglist))+" entries"
		return imglist

	def make_gif(self, killmax, imglist, dir=None):
		if dir == "gif":
                        gifName = 'latest.gif'
			gifPath = os.path.join(os.getcwd(), dir, gifName)
                if dir == "gif_map":
                        gifName = 'latest_map.gif'
			gifPath = os.path.join(os.getcwd(), dir, gifName)
		#produce a gif of the last 10 images when self.count == 10
		print "Producing gif image"
		if os.path.isfile(gifPath):
			os.remove(gifPath)
	
		print gifName, gifPath	
		#command = "convert -delay 40 -loop 0 "+os.getcwd()+"/"+dir+"/*.png -gravity center -fill white -annotate -100+100 '%f' latest.gif"
		command = "nice -5 convert -limit memory 1G -delay 40 -loop 0 "+os.getcwd()+"/"+dir+"/*.png " + gifName
		print command
		out = subprocess.Popen(command, stdout = subprocess.PIPE, shell=True)
		stdoutp, stderrp = out.communicate()
		print stdoutp
		if os.path.isfile(gifName):
			print "gif image produced"
			shutil.copyfile(gifName, os.path.join("/var/www/html/", gifName))
			self.uploadImg(gifName)
		else:
			print "gif was not created"
		return

	def makeMPEG(self, killmax, imglist, dir=None):

	def uploadImg(self, img):
		try:
                	self.trans.openConnection()
                        if os.path.isfile(img):
                                self.trans.uploadFile(img)
	              	self.trans.closeConnection()
                except:
                	print "could not connected to remote server"
			traceback.print_exc()


if __name__ ==  "__main__":
	cg = CloudGif()
	
	while True:
		subDir = 'gif'
		subDir2 = 'gif_map'
		cg.cleanDir(subDir)
		cg.cleanDir(subDir2)
		try:
			l = cg.findImg(subDir)
			imgList = sorted(l)
		except:
			traceback.print_exc()
		"""try:
			l2 = cg.findImg(subDir2)
                        imgList2 = sorted(l2)
                except:
                        traceback.print_exc()
		"""

		cg.make_gif(180, imgList, subDir)
		#cg.make_gif(180, imgList2, subDir2)
		time.sleep(180)
