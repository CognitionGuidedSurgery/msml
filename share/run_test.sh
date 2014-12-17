#!/bin/bash -x

pwd 

export PYTHONPATH=./cbuild/bin/:/home/ubuntu/msml/cache/VTK-6.1.0-BUILD/Wrapping/Python/:/home/ubuntu/msml/cache/VTK-6.1.0-BUILD/lib/

cd /home/ubuntu/msml/

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

