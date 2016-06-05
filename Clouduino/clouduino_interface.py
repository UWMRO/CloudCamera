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

class ClouduinoInterface():
    def __init__(self):
	self.ser = None
	self.serPort = 'dev/tty.usbserial'

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
        return

    def closePort(self):
	""" close the serial port connection to the arduino"""
        self.ser.close()
        return

   def readSer(self):
	""" Read in the arduino output, parse, and return something useful
	Arguments:
		None
	Returns:
		s (string): parsed serial output
	"""
        s = self.ser.readline()
        return s

   def getLux(self):
	""" calls the arduino getLux() function
	Arguments:
		None
	Returns:
		flux (float): flux level from light sensor
	"""
	self.ser.write('l')
	flux = float(self.readSer())  # this needs some error checking, I could see it causing problems later
	print flux
	return flux

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
	
   def getDomeStatus(self):
	"""returns the dome metrology in format humidity,temp,pos
	Arguments:
		None
	Returns:
		

	"""
	self.ser.write('d')
	time.sleep(1)
	line = self.ser.readline()
	l = line.split()
	print l
	return l

if __name__ == "__main__":
	c = ClouduinoInterface()
	c.openPort()
	time.sleep(1)
	c.getDomeStatus()
	time.sleep(1)
	c.closePort()
