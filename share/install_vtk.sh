#!/bin/sh

ARCHIV=VTK-6.1.0.tar.gz
URL=http://www.vtk.org/files/release/6.1/$ARCHIV
DIRNAME=VTK-6.1.0
BUILD_DIR=$DIRNAME-BUILD

# INSTALL VTK automatically

mkdir -p cache
cd cache

# get dump

if [ ! -f $ARCHIV ]; then
    wget $URL -O $ARCHIV
fi

if [ ! -d $DIRNAME ]; then
    tar xf $ARCHIV
fi

if [ ! -d $BUILD_DIR ]; then
    mkdir $BUILD_DIR
    cd $BUILD_DIR
    cmake ../$DIRNAME
    make -j 2
    cd ..
fi
