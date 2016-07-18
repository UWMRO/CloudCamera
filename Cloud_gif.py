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

class CloudGif(object):
	def __init__(self):
		self.trans = transfer()

	def findImg(self, dir = None):
	       	listdirect = os.path.join(os.getcwd(),'gif/')
	        imagelist = listdirect+'giflist.txt'

        	print "Creating a list of png files in gif/"
        	imglist = []
        	for img in os.listdir(listdirect):
                	if img.endswith(".png"):
                        	img = "gif/"+img
                        	imglist.append(img)
        	if len(imglist) == 0:
                	print "No images found in gif/"
                	print "Ending Cloud_gif.py"
			return
        	f = open(imagelist, "w")
        	f.write("\n".join(map(lambda x: str(x), imglist)))
        	f.close()

        	img_list = np.genfromtxt(imagelist, usecols = [0], unpack = True, dtype = 'str')
        	print "gif list has "+str(len(img_list))+" entries"
		return

	def make_gif(self, killmax, imglist):
		#produce a gif of the last 10 images when self.count == 10
		print "Producing gif image"
		killcount = 0
		if os.path.isfile('latest.gif'):
			os.remove("latest.gif")
		'''
		command = "convert -delay 40 -loop 0 "+os.getcwd()+"/gif/*.png latest.gif"
		out = subprocess.Popen(command, stdout = subprocess.PIPE, shell=True)
		stdoutp, stderrp = out.communicate()
		while stdoutp == None:
			print "subprocess output:"+str(stdoutp)
			if killcount == killmax:
				stdoutp = "ran out of time"
			else:
				print "gif not ready"
				print str(killcount)
				killcount += 1
				time.sleep(1)
		'''

		images = [Image.open(fn) for fn in imglist]
		writeGif('latest.gif', images, duration=0.5, subRectangles=False)

		#print "sleeping while gif is produced"
		#time.sleep(120)
		#writeGif("latest.gif", self.imglist, duration=0.3, repeat=True)
		if os.path.isfile('latest.gif'):
			print "gif image produced"
			shutil.copyfile("latest.gif", "/var/www/html/latest.gif")
			#upload = threading.Thread(self.uploadImg('latest.gif'))
			#upload.start()
			self.uploadImg('latest.gif')
		else:
			print "gif was not created"
		return

	def uploadImg(self, img):
		try:
                	self.trans.openConnection()
                        if os.path.isfile(img):
                                print 'uploading',str(img)
                                self.trans.uploadFile(img)
				time.sleep(30)
	              	self.trans.closeConnection()
                except:
                	print "could not connected to remote server"
			traceback.print_exc()


if __name__ ==  "__main__":
	cg = CloudGif()
	
	while True:
		l = cg.findImg('gif')
		imgList = sorted(l)
		cg.make_gif(180, imgList)

