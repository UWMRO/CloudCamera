#! /usr/bin/python

"""
clouduino_interface2_1.py

This program is designed to read in data from an arduino.
Specifically this is program interfaces to the arduino on the
cloud camera.  Functionality includes reading the temperature,
 humidity, and light levels.

TODO:
finish interface

Usage:

Options:


"""

__author__ = ["Joseph Huehnerhoff", "Matt Armstrong", "Andrew Wilkins"]
__license__ = "GPL"
__version__ = "0.1"
__maintainer__ = "Matt Armstrong"
__email__ = ""
__status__ = "Developement"

import serial
import datetime
import time
import os

class ClouduinoInterface():
    def __init__(self):
	self.ser = None
	#self.serPort = '/dev/tty.usbmodem1421'
    	self.serPort = '/dev/ttyACM0'
	self.savefile = os.getcwd()+'/logs/log.txt'
	
	self.heatCount = 0
	self.heatToggle = 5
	self.heatStatus = 0
	self.delay = 0.1

    def readSer(self):
    	"""
    	Check the serial port for data
    	and write any data with a timestamp
    	to the savefile
    	"""
        data = self.ser.readline().rstrip("\n").rstrip("\r")
    	f = open(self.savefile, 'a')
	timestamp = datetime.datetime.now().strftime("%Y%m%d-%H:%M:%S")
    	returnData = str(data)+",timestamp="+timestamp
	f.write(returnData)
    	f.close()
        return returnData

    def openPort(self):
	""" open the serial port for communication with the arduino"""
        self.ser=serial.Serial(self.serPort, 9600)
        return

    def closePort(self):
	""" close the serial port connection to the arduino"""
        self.ser.close()
        return

    def heatOn(self):
	self.ser.write(b'h')
	self.heatStatus = 1
	return

    def heatOff(self):
	self.ser.write(b'l')
	self.heatStatus = 0
	return

    def sortOutput(self, serDat = None):
        sortedDat = {}
	#print serDat
        #rawDat = serDat.strip('\r\n')
        #print rawDat
        sortedDat = dict(x.split('=') for x in serDat.split(','))
        return sortedDat


    def run(self):
        #self.openPort()
	data = ''
        data = self.readSer()
	#print data
	if data.startswith('heat=') == True:
	    self.heatCount += 1
            print self.sortOutput(data)
	    if self.heatToggle == self.heatCount:
		if self.heatStatus == 0:
		    self.heatOn()
		    print "Heat on"
		    #time.sleep(5)
		else:
		    self.heatOff()
		    print "Heat off"
		    #time.sleep(5)
		self.heatCount = 0	
	    time.sleep(self.delay)
	else:
	    time.sleep(0.2)
        #self.closePort()

if __name__ == "__main__":
	c = ClouduinoInterface()
	run = True
    	c.openPort()
	time.sleep(2)
    	while run == True:
        	c.run()
    	#c.closePort()
