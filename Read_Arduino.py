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

ser = serial.Serial('dev/tty.usbserial', 2400)  #Connect to serial port 2400
savefile = str(time.strftime("%Y%m%d")+"_arduino.txt")	#Name log file: <date>_arduino.txt

while True:
    """
    Check the serial port for data
    and write any data with a timestamp
    to the savefile
    """
    data = ser.readline()
    f = open(savefile, 'a')
    f.write(str(time.strftime("%H%M%S"))+","+str(data))
    f.close()
