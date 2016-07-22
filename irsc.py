#! /usr/bin/python

from astropy.time import Time
import transfer
import time
import datetime as dt

class IRSC(object):
	def __init__(self):
		self.server = 'irsc.apo.nmsu.edu'
		self.usr = 'irsc'

	def latestImg(self):
		t = transfer.transfer()
		utcDay = dt.datetime.utcnow()
		currentMJD = int(Time(utcDay.strftime("%Y-%m-%d"), format='isot').mjd)
		#currentMJD = '57592'
		print currentMJD
		files = t.findFiles(self.server,self.usr, 'data/'+str(currentMJD))
		#print sorted(files)
		if files != False:
			#for f in files:
			#	print 'do something'	
			pass
		return


if __name__ == "__main__":
	i = IRSC()
	i.latestImg()	
