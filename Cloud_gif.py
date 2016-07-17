'''
CloudCam gif production routine
'''
import os
import subprocess
import time
import shutil
from transfer import transfer
 
class CloudGif(object):
	def __init__(self):
		self.trans = transfer()

	def make_gif(self, killmax):
		#produce a gif of the last 10 images when self.count == 10
		print "Producing gif image"
		killcount = 0
		if os.path.isfile('latest.gif'):
			os.remove("latest.gif")
		command = "convert -delay 40 -loop 0 "+os.getcwd()+"/gif/*.png latest.gif"
		out = subprocess.Popen(command, stdout = subprocess.PIPE, shell=True)
		stdoutp, stderrp = out.communicate()
		while stdoutp == None:
			print "subprocess output:"+str(stdoutp)
			if killcount == killmax:
				stdoutp = "ran out of time"
			else:
				print "gif not ready"
				killcount = 60
				time.sleep(1)
		#print "sleeping while gif is produced"
		#time.sleep(120)
		#writeGif("latest.gif", self.imglist, duration=0.3, repeat=True)
		if os.path.isfile('latest.gif'):
			print "gif image produced"
			shutil.copyfile("latest.gif", "/var/www/html/latest.gif")
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
                	self.trans.closeConnection()
                except:
                	print "could not connected to remote server"
			traceback.print_exc()


if __name__ ==  "__main__":
	cg = CloudGif()
	cg.make_gif(60)

