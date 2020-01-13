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
	self.dependencyList = ['libusb-dev', 'libtool', 'eclipse-cdt-autotools',
			       'python-matplotlib', 'python-astropy', 'python-scipy',
			       'python-pyfits']

    def run_setup(self):
	print("Welcome to the CloudCam setup routine.")
	print(" ")
	print("This program will install the needed dependencies and set up permissions to run the CloudCam.")

	demoMode = raw_input("Would you like to use the demonstration mode? (Yes/No or Y/N):")
	if demoMode.lower() in self.yesList:
	   print("Running software in Demo mode")
	   self.Demo = True
	else:
	   print("NOT using Demo mode, this will actually run terminal commands to install software.")
	   self.Demo = False

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
	print("CloudCam software can be set as a linux service, which will start the software automatically and keep it running through crashes.")
	serviceInstall = raw_input("Would you like to set CloudCam as a service? (Yes/No or Y/N):")
        if serviceInstall.lower() in self.yesList:
           self.services()
        else:
           print("NOT setting CloudCam as a service")

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
	if self.Demo == True:
	   print("DEMO MODE, NOT ACTUALLY RUNNING THESE COMMANDS:")
	   for i in range(len(self.dependencyList)):
              print("sudo apt-get install -y %s" %self.dependencyList[i])
	else:
	   print("Installing dependencies")
	   for i in range(len(self.dependencyList)):
	      self.runCmd("sudo apt-get install -y %s" %self.dependencyList[i])
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
	    self.runCmd("sudo usermod -a -G dialout $USER")
	    self.runCmd("g++ camera.cpp -lusb -lopenssag -o camera")
	return

    def services(self):
	print("Setting CloudCam as a service.")
	if self.Demo == True:
	   print("DEMO MODE, NOT ACTUALLY RUNNING THESE COMMANDS:")
	   print("sudo ln -s install/services/CloudCam.service /lib/systemd/system/CloudCam.service")
	   print("sudo ln -s install/services/CloudCam.service /lib/systemd/system/wiggleCloud.service")
	   print("sudo systemctl daemon-reload")
	   print("sudo systemctl enable CloudCam.service")
	   print("sudo systemctl enable wiggleCloud.service")
	else:
	   self.runCmd("sudo ln -s install/services/CloudCam.service /lib/systemd/system/CloudCam.service")
	   self.runCmd("sudo ln -s install/services/CloudCam.service /lib/systemd/system/wiggleCloud.service")
	   self.runCmd("sudo systemctl daemon-reload")
	   self.runCmd("sudo systemctl enable CloudCam.service")
	   self.runCmd("sudo systemctl enable wiggleCloud.service")
	   print("CloudCam is now a service")
	return

    def webserver(self):
	print("Setting up local webserver")
	if self.Demo == True:
	   print("DEMO MODE, NOT ACTUALLY RUNNING THESE COMMANDS:")
	   print("sudo apt-get -y install apache2")
	   print("sudo rm /var/www/html/index.html")
	   print("sudo cp index.html /var/www/html/index.html")
	else:
	   self.runCmd("sudo apt-get -y install apache2")
	   self.runCmd("sudo rm /var/www/html/index.html")
	   self.runCmd("sudo cp index.html /var/www/html/index.html")
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
	   self.runCmd("mkdir -p $HOME/.ssh")
	   self.runCmd("sudo chmod 0700 $HOME/.ssh")
	   self.runCmd("ssh-keygen -t rsa")
	   sshServer = raw_input("SSH key created, please enter the server you wish to connect to:")
           sshUser = raw_input("Please enter the username for the remote server:")
           self.runCmd("ssh-copy-id -i $HOME/.ssh/id_rsa.pub %s@%s" %(sshUser, sshServer))
	return

    def runCmd(self, command):
	print("Running command: %s" %command)
	process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
	process.wait()
	outs, err = process.communicate()
	print(outs)
	print(process.returncode)
	return

if __name__ == "__main__":
    cs = CloudSetup()
    
    cs.run_setup()

