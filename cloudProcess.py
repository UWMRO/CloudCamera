#! /etc/bin/python

import os, time, subprocess, re
def indProc():
	arr=[]
	p=subprocess.Popen(['ps -aux | grep CloudCam.py'],shell=True, stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	q=p.stdout.readlines()
	run_cam=False
	for x,f in enumerate(q):
		u=f.split()
		if  re.search('/home/cloudcam/CloudCamera/CloudCam.py', u[11]):
			run_cam=True

	p=subprocess.Popen(['ps -aux | grep wiggleCloud.py'],shell=True, stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        q=p.stdout.readlines()
        run_gif=False
        for x,f in enumerate(q):
                u=f.split()
                if re.search('/home/cloudcam/CloudCamera/wiggleCloud.py', u[11]):
                        run_gif=True

	p=subprocess.Popen(['ps -aux | grep clouduino_interface.py'],shell=True, stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        q=p.stdout.readlines()
        run_rain=False
        for x,f in enumerate(q):
                u=f.split()
                if re.search('/home/cloudcam/CloudCamera/clouduino_interface.py', u[11]):
                        run_rain=True


	return [run_cam,run_gif,run_rain]

def startProc(camStart = False, gifStart = False, rainStart = False):

	if camStart:
		print 'starting cloud cam'
		os.system('nohup python /home/cloudcam/CloudCamera/CloudCam.py &')
	if gifStart:
		print 'starting gif'
                os.system('nohup python /home/cloudcam/CloudCamera/wiggleCloud.py &')
	if rainStart:
                print 'starting Rain Sensors'
                os.system('nohup python /home/cloudcam/CloudCamera/clouduino_interface.py &')
	return	
	

if __name__ == "__main__":
	x=0
	y=0
	while True:
		arrProc=indProc()
		if x==5 and not arrProc[1]:
			print 'starting wiggle'
			startProc(False, True, False)
			x=0
		if y==5:
			print 'running rsync'
			p1 = subprocess.Popen(['rsync -azrh --progress --remove-source-files /home/cloudcam/CloudCamera/images/ analysis:/raid/CloudCamera/fits/'], stdout=subprocess.PIPE, shell=True)
			#print p1.stdout.read()
			p2 = subprocess.Popen(['rsync -azrh --progress --remove-source-files /home/cloudcam/CloudCamera/analyzed/ analysis:/raid/CloudCamera/'], stdout=subprocess.PIPE, shell=True)
			#print p2.stdout.read()
			y=0
		if not arrProc[0]:
			print 'start cloudcam'
			startProc(True, False)
		if not arrProc[2]:
			print 'starting clouduino_interface.py'
			startProc(False, False, True)
		x = x + 1
		y = y + 1
		time.sleep(60)
