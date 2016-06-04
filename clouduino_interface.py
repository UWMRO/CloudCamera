"""
This program is designed to read in
data from an arduino through serial
port 2400. Specifically this reads
the current temperature, humidity
and light levels. This data is saved
in a txt file that can be read later.
"""

import numpy as np
import serial
import datetime



class ClouduinoInterface():
    def __init__(self):
	self.ser = None
	self.serPort = 'dev/tty.usbserial'
	#savefile = str(time.strftime("%Y%m%d")+"_arduino.txt")	#Name log file: <date>_arduino.txt

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

    def openPort(self, event):
        self.ser=serial.Serial(self.serPort, 9600)
        return

    def closePort(self, event):
        self.ser.close()
        return

   def readSer(self):
	"""usually I make this a parser function that is specific to the device"""
        s = self.ser.readline()
        return s


