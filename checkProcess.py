#! /etc/bin/python

import os, time, subprocess, re
def indProc():
	arr=[]
	p=subprocess.Popen(['ps -aux | grep CloudCam.py'],shell=True, stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	q=p.stdout.readlines()
	run_cam='no'
	for x,f in enumerate(q):
		u=f.split()
		print u
		if  re.search('/home/cloudcam/CloudCamera/CloudCam.py', u[11]):
			run_cam='yes'

	p=subprocess.Popen(['ps -aux | grep Cloud_gif.py'],shell=True, stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        q=p.stdout.readlines()
        run_gif='no'
        for x,f in enumerate(q):
                u=f.split()
		print u
                if re.search('/home/cloudcam/CloudCamera/Cloud_gif.py', u[11]):
                        run_gif='yes'


	if run_cam=='no':
		print 'starting cloud cam'
		os.system('nohup python /home/cloudcam/CloudCamera/CloudCam.py &')
		run_cam='yes'
	if run_gif=='no':
		print 'starting gif'
                os.system('nohup python /home/cloudcam/CloudCamera/Cloud_gif.py &')
		run_gif='yes'
	
	return [run_cam,run_gif]

def outputCurrent():
	proc_arr=indProc()
	f=open('output.txt','w')
	f.writelines(time.strftime('#-------------------------\n%m/%d/%y  %H:%M:%S\n'))
	f.writelines('CloudCam.py: %s\n' % proc_arr[0])
	f.writelines('Cloud_gif.py: %s\n' % proc_arr[1])
	f.close()
	os.system('ps aux | grep python >> output.txt')
	print time.strftime('%m/%d/%y  %H:%M:%S  tasks written to current ouput.txt')
	
def outputLog():
	date=time.strftime('%Y%m%d')
	if os.path.exists(time.strftime('/var/www/weather/outLog/%Y%m%d_output.log'))==False:
		f=open('/var/www/weather/outLog/%s_output.log' % date,'w')
		f.writelines('')
		f.close()
	else:

		proc_arr=indProc()
        	f=open('/var/www/weather/outLog/%s_output.log' % date, 'a')
        	f.writelines(time.strftime('#-------------------------\n%m/%d/%y  %H:%M:%S\n'))
       	 	f.writelines('Weather: %s\n' % proc_arr[0])
        	f.writelines('Face Detection: %s\n' % proc_arr[1])
        	f.writelines('Basic Camera: %s\n' % proc_arr[2])
        	f.writelines('Weather Plot: %s\n' % proc_arr[3])
        	f.writelines('Gas Plot: %s\n' % proc_arr[4])
		f.writelines('Picture Server: %s\n' % proc_arr[5])
        	f.writelines('Make Thumbnail: %s\n------------------\n' % proc_arr[6])
		f.close()
       	 	os.system('ps aux | grep python >> /var/www/weather/outLog/%s_output.log' % date)
        	os.system('df -h /dev/sda1 >> /var/www/weather/outLog/%s_output.log' % date)
        	os.system('du -h -s /var/www/weather/images/ >> /var/www/weather/outLog/%s_output.log' % date)
        	os.system('du -h -s /var/www/Pictures/ >> /var/www/weather/outLog/%s_output.log' % date)
        	print time.strftime('%m/%d/%y  %H:%M:%S  tasks written to log ouput.log')


x=0

outputCurrent()
#outputLog()
time.sleep(60)
while True:
	if x==30:
		outputCurrent()
		#outputLog()
		x=0
		time.sleep(60)
	else:
		proc_arr=indProc()
		time.sleep(60)
		x=x+1
