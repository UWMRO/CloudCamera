#! /usr/bin/python

"""
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
import shutil
from Modules.transfer import transfer


class ClouduinoInterface():
    def __init__(self):
        # self.ser: serial.Serial | None = None
        # self.serPort: str = '/dev/tty.usbmodem1421'
        self.serPort: str = '/dev/ttyACM0'
        self.savefile: str = os.getcwd()+'/logs/log.txt'
        self.tr: transfer = transfer()

        self.heatToggle: int = 0  # Allow heaters? 1=y, 0=n
        self.heatStatus: int = 0
        self.heatLast: datetime.datetime = datetime.datetime.strptime(
            "01012001-00:00:00", "%m%d%Y-%H:%M:%S")
        self.heatThreshold: float = 40.0  # Minimum pi core temp to turn on heaters
        self.heatDuration: float = 10  # Duration (in mins) to run heaters

        self.rainStatus: float = 0
        self.rainThreshold: float = 40  # percent rain detects in last 30 seconds
        self.rainLast: datetime.datetime = datetime.datetime.strptime(
            "01012001-00:00:00", "%m%d%Y-%H:%M:%S")
        self.rain10m: bool = False
        self.coretemp: int = int(
            float(open('/sys/class/thermal/thermal_zone0/temp').read()) / 1e3)
        self.delay = 4.0

    def readSer(self):
        """
        Check the serial port for data
        and write any data with a timestamp
        to the savefile
        """
        # print("in readSer")
        data = self.ser.readline().rstrip(b"\n").rstrip(b"\r")
        f = open(self.savefile, 'a')
        timestamp = datetime.datetime.now().strftime("%Y%m%d-%H:%M:%S")
        returnData = str(data)+",timestamp="+timestamp
        f.write(returnData)
        f.close()
        return returnData

    def openPort(self):
        """ open the serial port for communication with the arduino"""
        self.ser = serial.Serial(self.serPort, 9600)
        # time.sleep(1)
        # self.ser.write(b'y')
        # time.sleep(1)
        # print(self.ser.readline())
        return

    def closePort(self):
        """ close the serial port connection to the arduino"""
        self.ser.close()
        return

    def checkStatus(self) -> dict[str, int | str]:
        self.ser.write(b's')
        time.sleep(0.1)
        data = ''
        data = self.readSer()
        sortedDat: dict[str, int | str] = {}
        # print(data)
        if data.startswith('heat=') == True:
            sortedDat = self.sortOutput(data)
            if len(sortedDat) == 3:
                self.rainStatus = int(sortedDat['rain'])
                sortedDat["rain10m"] = str(self.rainCheck())
                self.coretemp = int(
                    float(open('/sys/class/thermal/thermal_zone0/temp').read()) / 1e3)
                sortedDat['coretemp'] = self.coretemp
                sortedDat = self.checkHeat(sortedDat)
                self.heatStatus = int(sortedDat['heat'])
                print(sortedDat)
        return sortedDat

    def checkHeat(self, statusDict):
        coreTemp = statusDict['coretemp']
        if self.heatToggle == 1:
            if coreTemp <= self.heatThreshold:
                # will keep heaters running until 10min after heat rises above threshold
                self.heatLast = datetime.datetime.now()
            heatCheck = datetime.datetime.now() - self.heatLast
            heatCheckmins = heatCheck.total_seconds() / 60
            # print(timeCheckmins)
            if heatCheckmins <= self.heatDuration:
                self.heatOn()
                statusDict['heat'] = 1
                # print("heaters on")
            else:
                self.heatOff()
                statusDict['heat'] = 0
                # print("heaters off")
        else:
            statusDict['heat'] = 0
        return statusDict

    def heatOn(self):
        self.ser.write(b'h')
        self.heatStatus = 1
        return

    def heatOff(self):
        self.ser.write(b'l')
        self.heatStatus = 0
        return

    def sortOutput(self, serDat: str | None = None) -> dict[str, int | str]:
        # sortedDat = {}
        # print(serDat)
        # rawDat = serDat.strip('\r\n')
        # print(rawDat)
        if serDat == None or serDat == "":
            return {}

        out: dict[str, int | str] = {}
        for entry in serDat.split(","):
            entry_split = entry.split("=")
            out[entry_split[0]] = int(entry_split[1])
        return out

    def rainCheck(self):
        # print(self.rainStatus)
        if self.rainStatus >= self.rainThreshold:
            self.rainLast = datetime.datetime.now()
            # print("Rain Detected")
        timeCheck = datetime.datetime.now() - self.rainLast
        timeCheckmins = timeCheck.total_seconds() / 60
        # print(timeCheckmins)
        if timeCheckmins <= 10:
            self.rain10m = True
        else:
            self.rain10m = False
        # "rain10m = "+str(self.rain10m)
        return self.rain10m

    def serOut(self, status, filename):
        directory = os.getcwd()+'/'+filename+'.txt'
        f_out = open(directory, 'w')
        for key in status:
            f_out.write(str(key)+"="+str(status[key])+'\r\n')
        f_out.close()
        shutil.copy(directory, '/var/www/html/'+filename+'.txt')
        self.tr.uploadFile('galileo.apo.nmsu.edu', 'jwhueh',
                           filename+'.txt', 'public_html/CloudCamera/')
        return


if __name__ == "__main__":
    c = ClouduinoInterface()
    run = True
    c.openPort()
    time.sleep(2)
    c.ser.write(b'l')
    print("Port open")
    while run == True:
        # print("in loop")
        statusDict = c.checkStatus()
        # print(len(statusDict))
        if len(statusDict) == 5:
            c.serOut(statusDict, 'testlog')
            time.sleep(c.delay)

        else:
            time.sleep(0.1)

    # c.closePort()
