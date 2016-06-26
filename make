sudo apt-get -y install libusb-dev
sudo apt-get -y install libtool
sudo apt-get -y install eclipse-cdt-autotools
sudo apt-get -y install python-matplotlib
sudo apt-get -y install python-astropy
sudo apt-get -y install python-scipy
sudo apt-get -y install python-pyfits
sudo apt-get -y install apache2
sudo apt-get -y install libusb-dev
sudo apt-get -y install libtool
sudo apt-get -y install eclipse-cdt-autotools
sudo apt-get -y install python-matplotlib
sudo apt-get -y install python-astropy
sudo apt-get -y install python-scipy
sudo apt-get -y install python-pyfits
sudo apt-get -y install apache2
sudo rm /var/www/html/index.html
sudo cp index.html /var/www/html/index.html

g++ camera.cpp -lusb -lopenssag -o camera
