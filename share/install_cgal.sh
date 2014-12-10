#!/bin/sh

mkdir -p cache
cd cache

# get dump

libcgal=libcgal10_4.2-5ubuntu1_amd64.deb
libcgaldev=libcgal-dev_4.2-5ubuntu1_amd64.deb

	
if [ ! -f $libcgal ]; then
	wget http://mirrors.kernel.org/ubuntu/pool/universe/c/cgal/libcgal10_4.2-5ubuntu1_amd64.deb
fi

if [ ! -f $libcgaldev ]; then
	wget http://mirrors.kernel.org/ubuntu/pool/universe/c/cgal/libcgal-dev_4.2-5ubuntu1_amd64.deb
fi

sudo apt-get install libboost-thread-dev libboost-system-dev libboost-program-options-dev libmpfr-dev  libmpfr4 libboost-program-options1.54-dev   libboost-program-options1.54.0
sudo dpkg -i $libcgal $libcgaldev
