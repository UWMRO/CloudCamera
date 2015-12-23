"""
CloudCam.py
=================================
Used to automatically operate the Cloud Camera hardware
==========================
Need to do:
- Automate camera exposure
    - Add more headers to FITS files
- Automate exposure time
- Operate cover motor
- Create command line over-ride
"""

import time
import subprocess
from camera import *
import thread
from logger import *
import numpy as np

class Guider(object):

    def __init__(self):
        self.expTime = .5 # Image exposure time in seconds, used when calling the
			              # CameraExpose object to take imagery
        self.c = CameraExpose() # CameraExpose object, used to take images
        self.l = Logger() #Logger class creates logfile of processes

    def run(self):
	       if self.takeRef == True or self.ref == None: #if you want a new ref image, this will be True
	          self.takeRef(self)
              while (self.quit != True):
                  self.l.logStr('GuidingStarted', self.logType)
                  imName = time.strftime("%Y%m%dT%H%M%S.fits")    #take image
                  self.takeImage('image',imName,self.expTime)
                  time.sleep(float(self.expTime) + self.readoutOffset) #sleep while reading out 
