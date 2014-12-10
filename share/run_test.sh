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

error=$? #save errorlevel 

echo "Submit Result:"
coveralls

exit $error
