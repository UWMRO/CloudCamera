<<<<<<< HEAD
sudo apt-get -y install libusb-dev
sudo apt-get -y install libtool
sudo apt-get -y install eclipse-cdt-autotools
sudo apt-get -y install python-matplotlib
sudo apt-get -y install python-astropy
sudo apt-get -y install python-scipy
sudo apt-get -y install python-pyfits
sudo apt-get -y install apache2
=======
sudo apt-get install -y libusb-dev
sudo apt-get install -y libtool
sudo apt-get install -y eclipse-cdt-autotools
sudo apt-get install -y python-matplotlib
sudo apt-get install -y python-astropy
sudo apt-get install -y python-scipy
sudo apt-get install -y python-pyfits
sudo apt-get install -y apache2
>>>>>>> b4254045cc14f40801328c666ca4c241cbd465f1
g++ camera.cpp -lusb -lopenssag -o camera
sudo rm /var/www/html/index.html
sudo cp index.html /var/www/html/index.html
