#!/bin/sh

ARCHIV=VTK-6.1.0.tar.gz
URL=http://www.vtk.org/files/release/6.1/$ARCHIV
DIRNAME=VTK-6.1.0
BUILD_DIR=$DIRNAME-BUILD
INSTALL_DIR=$(readlink -f cache/$DIRNAME-INSTALL)

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

#if [ ! -d $BUILD_DIR ]; then
    mkdir -p $BUILD_DIR
    cd $BUILD_DIR
    
    cmake ../$DIRNAME -DVTK_WRAP_PYTHON:BOOL=ON -DCMAKE_INSTALL_PREFIX:STRING=${INSTALL_DIR}
    make -j 6 
    cd ..
#fi

if [ ! -d $INSTALL_DIR ]; then
    cd $BUILD_DIR
    make install
    cd ..
fi


