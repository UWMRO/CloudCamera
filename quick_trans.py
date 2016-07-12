import os, time

while True:
	os.system("scp /var/www/html/*.png galileo:public_html/CloudCamera/")
	print time.strftime('sent:  %Y%m%dT%H%M%S')
	time.sleep(30)
