#!/bin/sh

SOFADIR=sofa
BUILD_DIR=$SOFADIR-build
# INSTALL SOFA automatically

mkdir -p cache
cd cache

# get dump

if [ ! -d $SOFADIR ]; then
    git clone --depth 1 git://scm.gforge.inria.fr/sofa/sofa.git $SOFADIR
fi

if [ ! -d $BUILD_DIR ]; then
    mkdir $BUILD_DIR
    cd $BUILD_DIR
    cmake ../$SOFADIR
    cmake ../$SOFADIR
    make -j 2
    cd ..
fi
