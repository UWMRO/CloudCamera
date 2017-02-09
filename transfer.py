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
from paramiko import SSHConfig



class transfer(object):
	def __init__(self):
		self.ssh = None
		self.ftp = None

	def openConnection(self, server = None, user = None):
		self.ssh = paramiko.SSHClient()

		# ssh config file
		config = SSHConfig()
		#config.parse(open('/Users/jwhueh/.ssh/config'))
		config.parse(open(os.path.join(os.path.expanduser('~'),'.ssh/config')))
		serv = config.lookup(server)
		if 'proxycommand' not in serv:
                	proxy = False
		else:
			try:
				proxy = paramiko.ProxyCommand(serv['proxycommand'])
			except:	
				proxy = False
				traceback.print_exc()
		keyfile = os.path.expanduser('~/.ssh/id_rsa')
		password = keyring.get_password('SSH', keyfile)
		key = paramiko.RSAKey.from_private_key_file(keyfile, password='mro2015')
		self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		if proxy:
			self.ssh.connect(serv['hostname'], username=serv['user'], pkey = key, timeout = 30, sock=proxy)
		else:
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

	def remoteCommand(self, server = None, user = None, command = None):
		print(time.strftime("%Y%m%dT%H%M%S  Connecting: "), command)
                self.openConnection(server, user)
                stdin, stdout, stderr = self.ssh.exec_command(command)
               	print (stdout.read())
		print(time.strftime("%Y%m%dT%H%M%S  Connection Closed"))
                self.closeConnection()


if __name__ == "__main__":
	t = transfer()
	#t.openConnection('galileo.apo.nmsu.edu','jwhueh')
	#t.closeConnection()
	t.uploadFile('galileo.apo.nmsu.edu', 'jwhueh', 'images/20170125/20170125T023451_10.000.fits', 'public_html/cgi-bin/')
	#t.downloadFile('galileo.apo.nmsu.edu', 'jwhueh', 'public_html/CloudCamera/test.png', 'test.png')
	#print (t.findFiles('irsc.apo.nmsu.edu', 'irsc', 'data/56916'))
	

