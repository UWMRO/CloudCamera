#! /usr/bin/python

"""
<<<<<<< HEAD
clouduino_interface.py
=======
clouduino_interface2_2.py
>>>>>>> c5ed227b3ad99bb7342e4de9cc1c888fb4362c99

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
	self.heatToggle = 20
	self.heatStatus = 0
	self.rainStatus = 0
	self.rainThreshold = 40 	#percent ran detects in last 30 seconds
	self.rainLast = datetime.datetime.strptime("01012001-00:00:00", "%m%d%Y-%H:%M:%S")	
	self.rain10m = False
	self.delay = 4.0

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

    def checkStatus(self):
	self.ser.write(b's')
	time.sleep(0.1)
	data = ''
        data = self.readSer()
	print data
	if data.startswith('heat=') == True:		
	    sortedDat = self.sortOutput(data)
	    if len(sortedDat) == 3:
	    	#print sortedDat
	    	self.rainStatus = int(sortedDat['rain'])
	    	self.heatStatus = int(sortedDat['heat'])
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


    def rainCheck(self):
	print self.rainStatus
        if self.rainStatus >= self.rainThreshold:
	    self.rainLast = datetime.datetime.now()
	    #print "Rain Detected"
	timeCheck = datetime.datetime.now() - self.rainLast
	timeCheckmins =  timeCheck.total_seconds() / 60
	print timeCheckmins
	if timeCheckmins <= 10:
	   self.rain10m = True
	else:
	   self.rain10m = False
	print "rain10m = "+str(self.rain10m)
	return
	
        #self.closePort()

if __name__ == "__main__":
	c = ClouduinoInterface()
	run = True
    	c.openPort()
	time.sleep(2)
    	while run == True:
	    try:
		c.checkStatus()        	
		c.rainCheck()
		time.sleep(c.delay)
	    except:
	    	time.sleep(0.1)
    	#c.closePort()
