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

dpkg -i $libcgal $libcgaldev
