#! /usr/bin/python
"""
Logger.py
Generic Logging Tool
"""

__author__ = "Joseph Huehnerhoff"
__copyright__ = "NA"
__credits__ = [""]
__license__ = "GPL"
__version__ = "0.1"
__maintainer__ = "NA"
__email__ = "NA"
__status__ = "Developement"

import time
import os

class Logger(object):
    def __init__(self):
        self.dir = os.path.join(os.getcwd(),'logs/')

    def logStr(self, line, dev):
        f_in = open(str(self.dir)+time.strftime("%Y%m%d_")+str(dev)+".log",'a')
        t = time.strftime("%Y%m%dT%H%M%S")
        f_in.write("%s\t%s\n" % (t, str(line)))
        f_in.close()
        return
