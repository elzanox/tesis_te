Install Open Vino

sudo apt-get purge wolfram-engine libreoffice* -y

sudo apt-get clean 
sudo apt-get autoremove -y

sudo apt-get update && sudo apt-get upgrade -y

sudo apt-get install build-essential cmake unzip pkg-config -y

sudo apt-get install libjpeg-dev libpng-dev libtiff-dev libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev libx264-dev libgtk-3-dev libcanberra-gtk* libatlas-base-dev gfortran python3-dev -y