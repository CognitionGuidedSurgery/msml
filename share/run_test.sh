#!/bin/bash -x
cd /home/ubuntu/msml/

export LD_LIBRARY_PATH=./cache/VTK-6.1.0-INSTALL/lib:$LD_LIBRARY_PATH
export PYTHONPATH=./cbuild/bin/:./cache/VTK-6.1.0-INSTALL/lib/python2.7/site-packages

echo "Nose Test:"
nosetests -vv --with-coverage  \
	--cover-tests              \
	--cover-inclusive          \
	--cover-package=msml       \
	--cover-erase              \
	-w src                     \
	msmltest

error1=$? #save errorlevel 

echo "Submit Result:"
coveralls


cd cbuild/ 
make test -j 2 
error2=$?
cp -R Testing/Temporary/ $CIRCLE_ARTIFACTS

exit $(( $error1 + $error2 ))

