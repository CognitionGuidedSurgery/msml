#!/bin/bash -x

pwd 

set

#source /home/ubuntu/virtualenvs/venv-2.7.5/bin

export PYTHONPATH=/home/ubuntu/msml/cbuild/bin

cd /home/ubuntu/msml/

echo "Nose Test:"
nosetests -vv --with-coverage --cover-tests --cover-inclusive --cover-package=msml --cover-erase -w src msmltest
error=$? #save errorlevel 

echo "Submit Result:"
coveralls

exit $error
