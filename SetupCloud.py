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

	print("----------------------------------------------")
	print("At this point, the basic setup is complete and the CloudCam can collect and process images.")
	print(" ")
	print("This script will help you set up different image delivery choices.")
	print("You can use SSH/SCP to push images to a remote server and/or you can use the CloudCam to run a local webpage to display the images.")
	print(" ")
	print("The first thing this script will help you set up is a local webserver to display images from the CloudCam.")
	webserverInstall = raw_input("Would you like to set up a local webserver? (Yes/No or Y/N):")
        if webserverInstall.lower() in self.yesList:
           self.webserver()
        else:
	   print("Skipping webserver setup.")

	print("----------------------------------------------")
	print("The CloudCam can also push images to a remote server using SCP and SSH keys.")
	scpInstall = raw_input("Would you like to set up SSH keys and SCP to a remote server? (Yes/No or Y/N):")
        if scpInstall.lower() in self.yesList:
           self.scpSetup()
        else:
           print("Skipping SCP setup.")

	print("----------------------------------------------")
	print("The CloudCam setup routine is now complete.")
	print("Please enjoy your CloudCam experience")
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

    def webserver(self):
	print("Setting up local webserver")
	if self.Demo == True:
	   print("DEMO MODE, NOT ACTUALLY RUNNING THESE COMMANDS:")
	   print("sudo apt-get -y install apache2")
	   print("sudo rm /var/www/html/index.html")
	   print("sudo cp index.html /var/www/html/index.html")
	else:
	   print("Setting up webserver")
	return

    def scpSetup(self):
	print("Setting up SSH keys and SCP to remote server")
	if self.Demo == True:
	   print("DEMO MODE, NOT ACTUALLY RUNNING THESE COMMANDS:")
	   print("mkdir -p $HOME/.ssh")
	   print("sudo chmod 0700 $HOME/.ssh")
	   print("ssh-keygen -t rsa")
	   sshServer = raw_input("SSH key created, please enter the server you wish to connect to:")
	   sshUser = raw_input("Please enter the username for the remote server:")
	   print("ssh-copy-id -i $HOME/.ssh/id_rsa.pub %s@%s" %(sshUser, sshServer))
	else:
	   print("Setting up SSH key and SCP")
	return

if __name__ == "__main__":
    cs = CloudSetup()
    
    cs.run_setup()

