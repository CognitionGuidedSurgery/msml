#!/bin/bash

BASE=tetgen1.5.0
DLNAME=$BASE.tar.gz
BUILD=tetgen-build

mkdir -p cache
cd cache

if [ -f $DLNAME ]; then
    wget  http://wias-berlin.de/software/tetgen/1.5/src/$DLNAME
fi

if [ -d $BASE ]; then
   tar xvfz $DLNAME
fi

if [ -d $BUILD ]; then
    mkdir $BUILD
    cd $BUILD
    cmake -DCMAKE_CXX_FLAGS:STRING="-fPIC -O3" ../$BASE
    make -j 2
fi
