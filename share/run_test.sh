#!/bin/bash -x

pwd 

export PYTHONPATH=./cbuild/bin/

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

