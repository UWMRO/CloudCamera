#! /user/bin/python
from __future__ import division  # this handles truncation 10/3. ==> 10/3
from __future__ import print_function
from __future__ import absolute_import # where it looks in the path for modules

"""
transfer.py
Upload Tool using Paramiko
"""

__author__ = "Joseph Huehnerhoff"
__copyright__ = "NA"
__credits__ = [""]
__license__ = "GPL"
__version__ = "0.1"
__maintainer__ = "NA"
__email__ = "NA"
__status__ = "Developement"

import paramiko
import time
import os

class transfer(object):
	def __init__(self):
		self.server = 'ovid.u.washington.edu'
		self.user = 'jwhueh'
		self.ssh = None
		self.ftp = None

	def openConnection(self, server = None, user = None):
		self.ssh = paramiko.SSHClient()
		self.ssh.set_missing_host_key_policy(
    		paramiko.AutoAddPolicy())
		self.ssh.connect(self.server, username=self.user)
		self.ftp = self.ssh.open_sftp()

	def uploadFile(self, f_in):
		#add changdir to public_html
		self.ftp.put(os.path.join(os.getcwd(), f_in), os.path.join('public_html/', f_in))
		return

	def closeConnection(self):
		self.ftp.close()
		self.ssh.close()
		return

if __name__ == "__main__":
	t = transfer()
	t.openConnection()
	t.uploadFile('make')
	time.sleep(1)
	t.closeConnection()
