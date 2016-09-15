#! /etc/bin/python
from __future__ import division  # this handles truncation 10/3. ==> 10/3
from __future__ import print_function
from __future__ import absolute_import # where it looks in the path for modules

"""
cloudProcess.py

Verify that the correct processes are running and if they fail unexpectedly restart them.

TODO:
	- This code could use a massive rewrite, it is quick and dirty.
	- There is a mix of subprocess and os imports.  All the os calls should be changed to subprocess calls.

Usage:
	nohup python cloudProcess.py &

Updates:

"""

import os
import time
import subprocess
import re

class CheckProcess(object):
	def __init__:
		"""
		init function for some future use
		"""
		pass

	def indProc(self):
		"""
		check on the status of a set of processes.  Could probably make this a for loop looking throug ha dictionary
		Args:
			None
		Returns:
			array: running processes
		"""
			
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

	def startProc(self, camStart = False, gifStart = False, rainStart = False):
		"""
		Start a process based on input
		Args:
			camStart (bool): True if CloudCam.py should be started
			gifStart (bool): True if wiggleCloud.py should be started
			rainStart (bool): True if clouduino_interface.py should be started	
		Returns:
			None
		"""
		if camStart:
			print ('starting cloud cam')
			os.system('nohup python /home/cloudcam/CloudCamera/CloudCam.py &')
		if gifStart:
			print ('starting gif')
                	os.system('nohup python /home/cloudcam/CloudCamera/wiggleCloud.py &')
		if rainStart:
                	print ('starting Rain Sensors')
                	os.system('nohup python /home/cloudcam/CloudCamera/clouduino_interface.py &')
		return	
	

if __name__ == "__main__":
	c = CheckProcess()
	x=0
	y=0
	while True:
		arrProc=c.indProc()
		if x==5 and not arrProc[1]:
			print ('starting wiggle')
			c.startProc(False, True, False)
			x=0
		if y==5:
			print ('running rsync')
			p1 = subprocess.Popen(['rsync -azrh --progress --remove-source-files /home/cloudcam/CloudCamera/images/ analysis:/raid/CloudCamera/fits/'], stdout=subprocess.PIPE, shell=True)
			#print p1.stdout.read()
			p2 = subprocess.Popen(['rsync -azrh --progress --remove-source-files /home/cloudcam/CloudCamera/analyzed/ analysis:/raid/CloudCamera/'], stdout=subprocess.PIPE, shell=True)
			#print p2.stdout.read()
			y=0
		if not arrProc[0]:
			print ('start cloudcam')
			c.startProc(True, False)
		if not arrProc[2]:
			print ('starting clouduino_interface.py')
			c.startProc(False, False, True)
		x = x + 1
		y = y + 1n
		time.sleep(60)
