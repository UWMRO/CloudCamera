#! /usr/bin/python

"""
clouduino_interface.py
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
import time
import os

class ClouduinoInterface():
    def __init__(self):
	self.serPort = '/dev/ttyACM0'

    def log(self):
    	"""
    	Check the serial port for data
    	and write any data with a timestamp
    	to the savefile
    	"""
    	data = ser.readline()
    	f = open(savefile, 'a')
    	f.write(str(time.strftime("%H%M%S"))+","+str(data))
    	f.close()

    def openPort(self):
	""" open the serial port for communication with the arduino"""
        self.ser=serial.Serial(self.serPort, 9600)
        self.readSer()
	return

    def closePort(self):
	""" close the serial port connection to the arduino"""
        self.ser.close()
        return

    def checkRain1(self):
	""" Check the status of the rain sensor"""
        self.ser.write('r')
        time.sleep(1)
        status = self.readSer()
	if status == "rain1 = True":
            #print "rain1 = true"
	    return True
        elif status == "rain1 = False":
            #print "rain1 = False"
	    return False
        else:
	    #print status
            return None

    def checkRain2(self):
        """ Check the status of the rain sensor"""
        self.ser.write('t')
        time.sleep(1)
        status = self.readSer()

        if status == "rain2 = True":
            return True
        elif status == "rain2 = False":
            return False
        else:
            return None


    def checkRain(self):
        """ Check the status of the rain sensor"""
	rain1 = self.checkRain1()
	rain2 = self.checkRain2()
	print time.strftime("%Y%d%mT%H%M%SMDT"),rain1, rain2
        if rain1 == False and rain2 == False:
            return False
        else:
            return True



    def readSer(self):
	""" Read in the arduino output, parse, and return something useful
	Arguments:
		None
	Returns:
		s (string): parsed serial output
	"""
	s = self.ser.readline().rstrip("\n").rstrip("\r")
	#print s
        return s

    def setFilterPos(self, pos):
	""" pos accepts True or False.  If true then it moves into position
	Arguments:
		pos (bool): True if filter should be in path, False if not
	Retruns:
		None
	"""
	if pos:
		self.ser.write('i')
	else:
		self.ser.write('o')
	return


    def rainOut(self, status = None):
	f_out = open(os.path.join(os.getcwd(),'rain.dat'),'w')
	f_out.write(str(status))
	f_out.close()

if __name__ == "__main__":
	c = ClouduinoInterface()
	c.openPort()
	time.sleep(1)
	print 'port open'
	while True:
		c.rainOut(c.checkRain())	
		time.sleep(5)
	c.closePort()
