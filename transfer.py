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

class transfer(object):
	def __init__(self):
		self.parm = self.retrieveParm()
		self.ssh = "galileo.apo.nmsu.edu"
		self.ftp = None

	def openConnection(self, server = None, user = None):
		self.ssh = paramiko.SSHClient()
		keyfile = os.path.expanduser('~/.ssh/id_rsa')
		password = keyring.get_password('SSH', keyfile)
		key = paramiko.RSAKey.from_private_key_file(keyfile, password='mro2015')
		self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		self.ssh.connect(self.parm['server'], username=self.parm['user'], pkey = key, timeout = 30)
		self.ftp = self.ssh.open_sftp()

	def transProgress(self, trans, toBeTrans):
		sys.stdout.write("\rtransferred: {0:.0f} %".format((trans / toBeTrans) * 100))
		sys.stdout.flush()


	def uploadFile(self, f_in):
		print("uploading: ", f_in)
		self.ftp.put(f_in,os.path.join(self.parm['server_dir'], f_in), callback=self.transProgress)
		print("")
		return

	def closeConnection(self):
		self.ftp.close()
		self.ssh.close()
		return

	def retrieveParm(self, f_loc = None):
		dict = {}
		f_in = open(os.path.join(os.getcwd(), 'transfer.init'),'r')
		for line in f_in:
			l = line.split()
			dict[l[0]] = l[1]
		f_in.close()
		return dict

if __name__ == "__main__":
	t = transfer()
	t.openConnection()
	t.uploadFile('/var/www/html/latest.png')
	t.closeConnection()
