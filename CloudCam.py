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
from Cloud_Graph import *
from camera import *
from logger import *
import datetime
from clouduino_interface import ClouduinoInterface

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

        self.min = 40.0
        self.max = 100.0
        self.step = 0.40
        self.expose = 1.0
        self.dir = os.path.join(os.getcwd(),'images')
        self.gain = 1
	self.filterpos = 0

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

        # Check and adjust exposure timing if necessary
        if median < self.min:
	    self.expose = self.expose*(1.0+self.step)
            print "Exposure too short, increasing by "+str(self.step*100)+"%"
        elif median > self.max:
            self.expose = self.expose*(1.0-self.step)
            print "Exposure too long, decreasing by "+str(self.step*100)+"%"
        else:
            print "Exposure within bounds"

        # If exposure reaches minimum, move the filter over the lens
        if self.expose < 0.02:
    	    if self.filterpos == 0:
        		print "Moving filter into FoV"
        		c.openPort()
        		time.sleep(2)
        		c.setFilterPos(False)
        		time.sleep(5)
        		c.closePort()
        		self.filterpos = 1
            else:
        		print "Exposure reached minimum of 0.02s"
        		self.expose = 0.02

        # if exposure reaches maximum, move the filter out of the way
    	if self.expose > 60.0:
    	    if self.filterpos == 1:
        		print "Moving filter out of FoV"
        		c.openPort()
        		time.sleep(2)
        		c.setFilterPos(False)
        		time.sleep(5)
        		c.closePort()
        		self.filterpos = 0
            else:
        		print "Exposure reached maximum of 60s"
        	        self.expose = 60.0
	    return

    def run_camera(self):
        """
        Take and analyze image, check exposure after analysis
        """

        name = time.strftime("%Y%m%dT%H%M%S")+"_"+str('%.3f'%(self.expose))
        print str('%.3f'%(self.expose))
        self.takeImage("cloud", name+".fits", self.expose, self.dir)
        time.sleep(self.expose+2)
        median = cg.run_analysis("images/"+name+".fits", "analyzed/"+name+"_analyzed.png", name)
        self.check_exposure(median)
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
        l = Logger()
        self.fakeOut =  False
        im = False
        if self.fakeOut != True:
            im = self.c.runExpose(str(imgName), str(imExp), str(imDir), self.gain)
            #l.logStr('Image\t%s %s %s' % (str(imgName), str(imExp), str(imDir)), self.logType)
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
