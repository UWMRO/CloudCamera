sudo apt-get install -y libusb-dev
sudo apt-get install -y libtool
sudo apt-get install -y eclipse-cdt-autotools
sudo apt-get install -y python-matplotlib
sudo apt-get install -y python-astropy
sudo apt-get install -y python-scipy
sudo apt-get install -y python-pyfits
sudo apt-get install -y apache2
g++ camera.cpp -lusb -lopenssag -o camera
sudo rm /var/www/html/index.html
sudo cp index.html /var/www/html/index.html
