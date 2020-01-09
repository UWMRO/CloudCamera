"""
SetupCloud.py
Sets up the CloudCam analysis software.
Installs dependencies required for CloudCam
Allows user to set up local webpage and/or SCP push to display images

TODO:


Usage:

"""
import os
import subprocess
from datetime import datetime

class CloudSetup(object):
    def __init__(self):
	self.Demo = True

	self.yesList = {'yes', 'y'}
	self.dependencyList = ['libusb-dev', 'libtool', 'eclipse-cdt-autools',
			       'python-matplotlib', 'python-astropy', 'python-scipy',
			       'python-pyfits']

    def run_setup(self):
	print("Welcome to the CloudCam setup routine.")
	print(" ")
	print("This program will install the needed dependencies and set up permissions to run the CloudCam.")
	
	beginSetup = raw_input("Would you like to begin setup? (Yes/No or Y/N):")
	if beginSetup.lower() in self.yesList:
	   print("Continuing setup routine")
           print("----------------------------------------------")
	else:
	   print("Exiting setup routine")
	   quit()

	print("The first step of this program will install the following software dependencies.")
	print("----------------------------------------------")
	for i in range(len(self.dependencyList)):
	   print(self.dependencyList[i])
        print("----------------------------------------------")
	dependencyInstall = raw_input("Would you like to install these dependencies? (Yes/No or Y/N):")
	if dependencyInstall.lower() in self.yesList:
	   self.dependencies()
        else:
           print("Exiting setup routine")
           quit()

	print("Next, we need to set up permissions for CloudCam hardware.")
	print("The following commands are required:")
	print("sudo usermod -a -G dialout $USER")
        print("g++ camera.cpp -lusb -lopenssag -o camera")
	print("----------------------------------------------")
	permissionInstall = raw_input("Would you like to set these permissions? (Yes/No or Y/N):")
        if permissionInstall.lower() in self.yesList:
           self.permissions()
        else:
           print("Exiting setup routine")
           quit()


	return

    def dependencies(self):
	print("Installing dependencies")
	if self.Demo == True:
	   print("DEMO MODE, NOT ACTUALLY RUNNING THESE COMMANDS:")
	   for i in range(len(self.dependencyList)):
              print("sudo apt-get install -y %s" %self.dependencyList[i])
	else:
	   print("Installing dependencies")
	print("Dependencies installed successfully.")
        print("----------------------------------------------")
	return

    def permissions(self):
	print("Setting up hardware permissions")
	if self.Demo == True:
	    print("DEMO MODE, NOT ACTUALLY RUNNING THESE COMMANDS:")
	    print("sudo usermod -a -G dialout $USER")
	    print("g++ camera.cpp -lusb -lopenssag -o camera")
	else:
	    print("Setting permissions")
	return

if __name__ == "__main__":
    cs = CloudSetup()
    
    cs.run_setup()

