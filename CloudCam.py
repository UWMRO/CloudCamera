import numpy as np
from Cloud_Graph import *
from camera import *
from logger import *
import datetime

class CloudCam(object):
    def __init__(self):
        self.min = 25.0
        self.max = 100.0
        self.step = 0.20
        self.expose = 1.0
        self.dir = os.path.join(os.getcwd(),'images')
        self.cg = CloudGraph()
        self.c = CameraExpose()

    def check_exposure(self, median):

        if median < self.min:
            self.expose = self.expose*(1.0+self.step)
            print "Exposure too short, increasing by "+str(self.step*100)+"%"
        elif median > self.max:
            self.expose = self.expose*(1.0-self.step)
            print "Exposure too long, decreasing by "+str(self.step*100)+"%"
        else:
            print "Exposure within bounds"

        if self.expose < 0.02:
	    print "Exposure reached minimum of 0.02s"
	    self.expose = 0.02
	return

    def run_camera(self):
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
            im = self.c.runExpose(str(imgName), str(imExp), str(imDir), int(1))
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
    img_list, static_mask = cg.start_up_checks()

    run = True
    while run == True:
        cc.run_camera()
