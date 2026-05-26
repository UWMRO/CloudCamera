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

import os
import typing
import traceback
import time

import numpy as np

import Modules.graphCloud as graphCloud
from Modules.camera import *
from Modules.clouduino_interface import ClouduinoInterface
import CloudParams


class CloudCam:
    _debug: typing.Final[bool] = True

    _min_med: float
    _max_med: float
    _step: float
    _exp: float
    _max_exp: float
    _gain: float
    _max_gain: float

    _filterpos: int

    _img_dir: str
    _backup_file: typing.Final[str] = "backupParams.txt"

    _cg: graphCloud.CloudGraph = graphCloud.CloudGraph()
    _cam: CameraExpose = CameraExpose()
    _cli: ClouduinoInterface = ClouduinoInterface()

    def __init__(self,
                 min_med: float,
                 max_med: float,
                 step: float,  # What percent the exp value changes under exposure control
                 exp: float,
                 max_exp: float,  # maximum median value for exposure control
                 gain: float,  # camera gain setting
                 max_gain: float,  # max camera gain (?)
                 filterpos: int,  # where is the filter arm? 0 = out, 1 = in
                 img_dir: str  # where are the .fits images saved
                 ):
        self._min_med = min_med
        self._max_med = max_med
        self._step = step
        self._exp = exp
        self._max_exp = max_exp
        self._gain = gain
        self._max_gain = max_gain
        self._filterpos = filterpos
        self._img_dir = img_dir

    def check_exposure(self, median):
        """
        Adjusts the exposure timing and filter arm position
        to try and keep the median between self._min_med and self._max_med

        input:
            median      (median value from analysis)
        """

        # Check and adjust exposure timing for low light
        print("bounds (minMed, maxMed, maxGain, maxExp: ",
              self._min_med, self._max_med, self._max_gain, self._max_exp)
        if median < self._min_med:
            if self._exp >= self._max_exp and self._gain >= 1:
                self._gain += 1
                if self._gain > self._max_gain:
                    self._gain = self._max_gain
                print("Gain Set To: "+str(self._gain))
            if self._exp <= self._max_exp and self._gain == self._max_gain:
                self._exp = self._exp*(1.0+self._step)
                print("Exposure too short, increasing to: " +
                      str(self._exp)+" seconds")

        # Check and adjust exposure and gain for high light
        elif median > self._max_exp:
            if self._exp >= 0.02 and self._gain > 1:
                self._gain -= 1
                print("Gain Set To: " + str(self._gain))
            if self._exp >= 0.02 and self._gain == 1:
                self._exp = self._exp*(1.0-self._step)
                print("Exposure too long, decreasing to: " +
                      str(self._exp)+" seconds")
        else:
            print("Exposure within bounds")
        if self._exp < 0.02:
            self._exp = 0.02
        if self._exp > self._max_exp:
            self._exp = self._max_exp
        try:
            backupParams = str(self._exp)+", "+str(self._gain)
            backup = open(self._backup_file, "w")
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

        # Check for fits image storage folder for today, make if needed
        if not os.path.isdir(os.path.join(os.getcwd(), 'images', dayDir)):
            os.mkdir(os.path.join(os.getcwd(), 'images'))
            os.mkdir(os.path.join(os.getcwd(), 'images', dayDir))
            print('directory made: ', os.path.join(
                os.getcwd(), 'images', dayDir))

        # Check for analyzed image storage folder for today, make if needed
        if not os.path.isdir(os.path.join(os.getcwd(), 'analyzed', dayDir)):
            os.mkdir(os.path.join(os.getcwd(), 'analyzed'))
            os.mkdir(os.path.join(os.getcwd(), 'analyzed', dayDir))
            print('directory made: ', os.path.join(
                os.getcwd(), 'analyzed', dayDir))
        return dayDir

    def run_camera(self):
        """
        Take and analyze image, check exposure after analysis
        """
        dayDir = os.path.join(os.getcwd(), 'images', self.checkDir())
        name = time.strftime("%Y%m%dT%H%M%S")+"_"+str('%.3f' % (self._exp))

        # Remove the old image binary file
        if os.path.isfile('binary'):
            os.remove('binary')

        try:
            backupParams = np.genfromtxt(self._backup_file, delimiter=",")
            self._exp = backupParams[0]
            self._gain = backupParams[1]
            # os.remove(self._backup_file)
        except:
            print("Could not load backup file")

        # Try to take an image
        try:
            self.takeImage("cloud", name+".fits", self._exp, dayDir)
        except:
            traceback.print_exc()
        if self._debug != True:
            time.sleep(self._exp+2)  # go to sleep while the image is taken

        # Run the analysis and check the exposure timing
        try:
            median = self._cg.run_analysis(os.path.join(
                dayDir, name), self._exp, self._gain)
            self.check_exposure(median)
        except:
            traceback.print_exc()
            # self._exp = 1.0
        if self._debug != True:
            if self._exp < 60:
                print(str(60-self._exp)+" seconds till next exposure")
                time.sleep(60-self._exp)

        return

    def takeImage(self, imType: str, imgName: str, imExp: float, imDir: str) -> int:
        """Takes the class, a string keyword for image type, a string for image
        name, an integer for exposure time, and a string for directory name.
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
        self.fakeOut = False
        im = False
        if self.fakeOut != True:
            print(imExp, self._gain)
            im = self._cam.runExpose(
                str(imgName), imExp, str(imDir), self._gain)
            if im == True:  # check on completion and save of image exposure
                time.sleep(1)
                return 0
            else:
                raise Exception("Image exposure not completed")
                return 1
        else:
            return 3  # Simply returns if no exception raised


if __name__ == "__main__":

    cg = graphCloud.CloudGraph()
    cg.start_up_checks()

    cc = CloudCam(CloudParams.min_median,
                  CloudParams.max_median,
                  CloudParams.step_size,
                  CloudParams.expose,
                  CloudParams.max_exp,
                  CloudParams.gain,
                  CloudParams.gainmax,
                  1,
                  "purr")

    FREQ_HZ: typing.Final[float] = 1
    run = True
    while run:
        start_t = time.time()
        cc.run_camera()
        # this line means that the next loop is called at every 1/freq seconds as opposed to 1/freq + execution time seconds
        time.sleep((time.time() + 1.0/FREQ_HZ) - start_t)
