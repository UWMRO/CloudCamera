sudo apt-get install libusb-dev
sudo apt-get install libtool
sudo apt-get install eclipse-cdt-autotools
sudo apt-get install python-matplotlib
sudo apt-get install python-astropy
sudo apt-get install python-scipy
sudo apt-get install python-pyfits
sudo apt-get install apache2
g++ camera.cpp -lusb -lopenssag -o camera
sudo rm /var/www/html/index.html
sudo cp index.html /var/www/html/index.html
