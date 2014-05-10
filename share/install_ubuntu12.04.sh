#!/bin/bash
# The Medical Simulation Markup Language (MSML) - Simplifying the biomechanical modeling workflow
# 
# MSML has been developed in the framework of 'SFB TRR 125 Cognition-Guided Surgery'
# 
# If you use this software in academic work, please cite the paper: 
#  S. Suwelack, M. Stoll, S. Schalck, N.Schoch, R. Dillmann, R. Bendl, V. Heuveline and S. Speidel,
#  The Medical Simulation Markup Language (MSML) - Simplifying the biomechanical modeling workflow,
#  Medicine Meets Virtual Reality (MMVR) 2014
#
# Copyright (C) 2013-2014 see Authors.txt
# 
# If you have any questions please feel free to contact us at suwelack@kit.edu
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#  
 

# Output information about system
lsb_release -a

# Use newer repository for vtk6.0
echo "deb http://de.archive.ubuntu.com/ubuntu trusty main restricted universe" \
	| sudo tee -a /etc/apt/sources.list

# DEBUG:
cat /etc/apt/sources.list

sudo apt-get update -y
sudo apt-get install -y libtet1.4.2 libtet1.4.2-dev \
			libxml2-dev  \
			libboost-filesystem-dev libboost-python-dev \
			libboost-program-options-dev libboost-graph-dev libboost-iostreams-dev \
			libcgal-dev \
			libvtk6 libvtk6-dev

echo "START with CMake:"
mkdir cbuild
cd cbuild 

#VCG not valid
cmake -DVTK_DIR=/usr/bin/ -DMODULES_VCGOperators=OFF -DVCG_INCLUDE_DIR:PATH="/usr/include/" ../operators

make -j 4
cd ..

sudo pip install nose coveralls
sudo pip install -r requirements.txt --use-mirrors

export PYTHONPATH=$(pwd)/src/
echo "Python Path: $PYTHONPATH"

cd src/msmltest
nosetests
#python ./test_analytics_export_rst.py
#python ./test_factory.py 
#python ./test_visitor_framework.py
