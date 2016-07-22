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
import keyring
import sys
import stat
import traceback

class transfer(object):
	def __init__(self):
		self.ssh = None
		self.ftp = None

	def openConnection(self, server = None, user = None):
		self.ssh = paramiko.SSHClient()
		keyfile = os.path.expanduser('~/.ssh/id_rsa')
		password = keyring.get_password('SSH', keyfile)
		key = paramiko.RSAKey.from_private_key_file(keyfile, password=password)
		self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		self.ssh.connect(server, username=user, pkey = key, timeout = 30)
		self.ftp = self.ssh.open_sftp()
		return

	def transProgress(self, trans, toBeTrans):
		sys.stdout.write("\rtransferred: {0:.0f} %".format((trans / toBeTrans) * 100))
		sys.stdout.flush()


	def uploadFile(self, server = None, user = None, f_in = None, server_dir = None):
		print(time.strftime("%Y%m%dT%H%M%S  Uploading:  "), f_in)
		self.openConnection(server, user)
		self.ftp.put(f_in,os.path.join(server_dir, f_in), callback=self.transProgress)
		self.closeConnection()
		print(time.strftime("\n%Y%m%dT%H%M%S  Connection Closed"))
		return

	def downloadFile(self, server = None, user = None, server_file = None, local_file = None):
		print(time.strftime("%Y%m%dT%H%M%S  Uploading:  "), server_file)
                self.openConnection(server, user)
                self.ftp.get(server_file, local_file, callback=self.transProgress)
                self.closeConnection()
                print(time.strftime("\n%Y%m%dT%H%M%S  Connection Closed"))
                return


	def findFiles(self, server = None, user = None, server_dir = None):
		print(time.strftime("%Y%m%dT%H%M%S  Looking in:  "), server_dir)
                self.openConnection(server, user)
		try:
			 self.ftp.stat(server_dir)
		except:
			traceback.print_exc()
			self.closeConnection()
			return False	
		files = self.ftp.listdir(server_dir)
		self.closeConnection()
                print(time.strftime("%Y%m%dT%H%M%S  Connection Closed"))
                return files

	def closeConnection(self):
		self.ftp.close()
		self.ssh.close()
		return

if __name__ == "__main__":
	t = transfer()
	#t.openConnection('galileo.apo.nmsu.edu','jwhueh')
	#t.closeConnection()
	#t.uploadFile('galileo.apo.nmsu.edu', 'jwhueh', 'test.png', 'public_html/CloudCamera/')
	#t.downloadFile('galileo.apo.nmsu.edu', 'jwhueh', 'public_html/CloudCamera/test.png', 'test.png')
	print (t.findFiles('irsc.apo.nmsu.edu', 'irsc', 'data/56916'))

