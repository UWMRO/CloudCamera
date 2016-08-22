#! /usr/bin/python

"""
CloudCam.py
Operates the CloudCam hardware and analysis software

TODO:


Usage:
    Automatic camera operation and data analysis from command line:
        python CloudCam.py

    Live data is displayed by opening a web browser and looking at
    the IP of the CloudCam
"""


import numpy as np
from graphCloud import *
from camera import *
import datetime
from clouduino_interface import ClouduinoInterface
import os
from CloudParams import *
import traceback

class CloudCam(object):
    def __init__(self):
        """
        Options:
            self.min        (minimum median value for exposure control)
            self.max        (maximum median value for exposure control)
            self.step       (What percent the exp value changes under exposure control)
            self.expose     (starting exposure length [s])
            self.dir        (where are the .fits images saved)
            self.gain       (camera gain setting)
            self.filterpos  (where is the filter arm? 0 = out, 1 = in)
        """

        self.min = min_median
        self.max = max_median
        self.step = step_size
        self.expose = expose
        self.dir = os.path.join(os.getcwd(),'images')
	self.dayDir = None
        self.gain = gain
	self.gainmax = gainmax
	self.backupFile = "backupParams.txt"

        self.cg = CloudGraph()
	self.c = CameraExpose()
	self.ci = ClouduinoInterface()


    def check_exposure(self, median):
        """
        Adjusts the exposure timing and filter arm position
        to try and keep the median between self.min and self.max

        input:
            median      (median value from analysis)
        """

	# Check and adjust exposure timing for low light
        if median < self.min:
	    if self.expose >=30.0 and self.gain >= 1:
                self.gain += 1
		if self.gain > self.gainmax:
			self.gain = self.gainmax
                print ("Gain Set To: "+str(self.gain))
            if self.expose <=60.0 and self.gain >= 1:
                self.expose = self.expose*(1.0+self.step)
                print ("Exposure too short, increasing to: "+str(self.expose)+" seconds")
	    if self.expose > 60.0:
		self.expose = 60.0

	# Check and adjust exposure and gain for high light
        elif median > self.max and self.expose != 60:
	    if self.expose >=0.02 and self.gain > 1:
            	self.gain -= 1
		print ("Gain Set To: "+ str(self.gain))
	    if self.expose >=0.02 and self.gain == 1:
		self.expose = self.expose*(1.0-self.step)
                print ("Exposure too long, decreasing to: "+str(self.expose)+" seconds")
        else:
            print ("Exposure within bounds")
	if self.expose < 0.02:
		self.expose = 0.02
	if self.expose > 60.0:
                self.expose = 60.0

	try:
		backupParams = str(self.expose)+", "+str(self.gain)
		backup = open(self.backupFile, "w")
		backup.write(backupParams)
		backup.close()
	except:
		print("Could not write backup file")

	return

    def checkDir(self):
	"""
	This function checks for needed image storage directories
	and creates them if necessary
	"""
	dayDir = time.strftime("%Y%m%d", time.gmtime())
	
	#Check for fits image storage folder for today, make if needed
	if not os.path.isdir(os.path.join(os.getcwd(), 'images', dayDir)):
		os.mkdir(os.path.join(os.getcwd(), 'images', dayDir))
		print ('directory made: ', os.path.join(os.getcwd(), 'images', dayDir))
	
	#Check for analyzed image storage folder for today, make if needed
	if not os.path.isdir(os.path.join(os.getcwd(), 'analyzed', dayDir)):
                os.mkdir(os.path.join(os.getcwd(), 'analyzed', dayDir))
		print ('directory made: ', os.path.join(os.getcwd(), 'analyzed', dayDir))
	return dayDir
	
    def run_camera(self):
        """
        Take and analyze image, check exposure after analysis
        """
	dayDir = os.path.join(os.getcwd(),'images',self.checkDir())
        name = time.strftime("%Y%m%dT%H%M%S")+"_"+str('%.3f'%(self.expose))

	#Remove the old image binary file
	if os.path.isfile('binary'):
		os.remove('binary')

	try:
                backupParams = np.genfromtxt(self.backupFile, delimiter=",")
                self.expose = backupParams[0]
                self.gain = backupParams[1]
                os.remove(self.backupFile)
        except:
                print("Could not load backup file")

	
	#Try to take an image
	try:
        	self.takeImage("cloud", name+".fits", self.expose, dayDir)
	except:
		traceback.print_exc()
        #time.sleep(self.expose+2)
	
	#Run the analysis and check the exposure timing
	try:
       		median = cg.run_analysis(os.path.join(dayDir,name), self.expose, self.gain)
		self.check_exposure(median)
	except:
		traceback.print_exc()
		self.expose = 1.0
	if self.expose < 60:
		print ("going to sleep for: "+str(60-self.expose)+" seconds")
		#time.sleep(60-self.expose)

        return

    def takeImage(self, imType = None, imgName = None, imExp = None, imDir = None):
        """Takes the class, a string keyword for image type, a string for image
        name, an integer for exposure tiem, and a string for directory name.
        The function checks if the variable fakeOut is equal to true first
        -- if so, ends function and carries out rest of code using existing
        images.  If not, the function takes an image using the CameraExpose
        object defined in the constructor, and checks that the image has
        been taken and saved.
        Args:
            imType (str): the type of image (bias, dark, object)
            imgName (str): the name of the image
            imExp (str): the exposure length in seconds
            imDir (str):  the directory of the image to be saved
        Returns:
            int.
            0 -- image was taken
            1 -- image not taken
            2 -- unknown state
        Raises:
            Exception
        """
        self.fakeOut =  False
        im = False
        if self.fakeOut != True:
            im = self.c.runExpose(str(imgName), str(imExp), str(imDir), self.gain)
            if im == True: # check on completion and save of image exposure
                time.sleep(1)
                return 0
            else:
                raise Exception("Image exposure not completed")
                return 1
        else:
            return 3 # Simply returns if no exception raised


if __name__ == "__main__":
    cg = CloudGraph()
    cc = CloudCam()
    cg.start_up_checks()

    run = True
    while run == True:
        cc.run_camera()
