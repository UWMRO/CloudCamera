'''
CloudCam gif production routine
'''

class CloudGif(object):
	def __init__(self):
		self.sleep = 120

	def make_gif(self):
		#produce a gif of the last 10 images when self.count == 10
		print "Producing gif image"
		killcount = 0
		if os.path.isfile('latest.gif'):
			os.remove("latest.gif")
		command = "convert -delay 40 -loop 0 "+os.getcwd()+"/gif/*.png latest.gif"
		out = subprocess.Popen(command, stdout = subprocess.PIPE, shell=True)
		stdoutp, stderrp = out.communicate()
		while stdoutp = None:
			print "subprocess output:"+str(stdoutp)
			if killcount == 60:
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

		plt.close("all")
		plt.close()
		return
