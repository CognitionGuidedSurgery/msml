#!/bin/sh

echo "Nose Test:"
nosetests -vv --with-coverage --cover-tests --cover-inclusive --cover-package=msml --cover-erase -w src msmltest
9 days
echo "Submit Result:"
coveralls
