# ======================================================================
# Given the 3D volume mesh of a mitral valve, this script computes
# - the bounds of bounding box,
# - the center of the bounding box,
# - the point in the middle of the top plane of the bounding box  (!!!)
# - the average 'radius' of the top plane of the bounding box     (!!!)
# for an automated setup of the HiFlow3-based MVR-Simulation.
# 
# NOTE: 3dvolumeMesh.vtu is called uGrid here.
# 
# How to run the script:
#   python mvGeometryAnalyzer.py 3dvolumeMesh.vtu analyticsOutputFilename.txt
# 
# Author: Nicolai Schoch, EMCL; 2015-04-12.
# ======================================================================

__author__ = 'schoch'
import numpy as np
import sys
import vtk
#from .msmlvtk import *  # not needed here; msmlvtk contains some rather specific vtk-functionalities...
from msml.log import error,info,debug,critical,fatal


def mvGeometry_Analyzer(inputfilename, ringFilename):
	# ======================================================================
	# get system arguments -------------------------------------------------
	ugFilename = inputfilename
	ringFilename_ = ringFilename
	outputFilename_ = "my_cool_mvGeometryAnalytics_outputfilename"
	
	print " "
	print "=================================================================================================="
	print "=== Execute Python script to analyze MV geometry in order for the HiFlow3-based MVR-Simulation ==="
	print "=================================================================================================="
	print " "
	#debug(" ")
	#debug("==================================================================================================")
	#debug("=== Execute Python script to analyze MV geometry in order for the HiFlow3-based MVR-Simulation ===")
	#debug("==================================================================================================")
	#debug(" ")
	
	# ======================================================================
	# read in files: -------------------------------------------------------
	# read in 3d valve mesh OR 3d ring mesh
	####vtureader = vtk.vtkXMLUnstructuredGridReader() # read vtu-MV
	###vtureader.SetFileName(ugFilename)
	vtureader = vtk.vtkXMLPolyDataReader() # read vtp-Ring
	vtureader.SetFileName(ringFilename_)
	vtureader.Update()
	uGrid = vtureader.GetOutput()
	
	# ======================================================================
	# compute bounding box, etc. -------------------------------------------
	# methods can be found in vtkDataSet
	
	# Get the center of the bounding box.
	center = np.zeros(3)
	uGrid.GetCenter(center)
	# Return a pointer to the geometry bounding box
	# (notation: [xmin,xmax, ymin,ymax, zmin,zmax].)
	bounds = np.zeros(6)
	uGrid.GetBounds(bounds)
	# compute point in the middle of top plane; raised by 0.5 * z-length of bounding box.
	midPtTop = np.zeros(3)
	midPtTop[0] = center[0]
	midPtTop[1] = center[1]
	midPtTop[2] = bounds[5] + 0.5 * (bounds[5]-bounds[4])
	# compute the average 'radius' of the top plane of the bounding box
	# compute x/y-distance-from-mid-to-border
	xDist = midPtTop[0] - bounds[0]
	yDist = midPtTop[1] - bounds[2]
	# compute average of x/y-distance-from-mid-to-border (corresponds to annulus radius)
	avDist = (xDist + yDist) / 2.0
	annulusRadius = avDist
	
	print "MV geometry analysis: DONE."
	#debug("MV geometry analysis: DONE.")
	
	# ======================================================================
	# write results to txt file --------------------------------------------
	f = open(outputFilename_, 'w')
	
	# produce outputAnalytics string and write into file
	analyticsString = 'midPtTop:(' + str(midPtTop[0]) + ',' + str(midPtTop[1]) + ',' + str(midPtTop[2]) + ');\n' + 'annulusRadius:' + str(annulusRadius) + ';\n'
	f.write(analyticsString)
	
	# close stream
	f.close()
	
	# ======================================================================
	print "Writing MVgeometryAnalyticsData output file: DONE."
	print "=================================================="
	print " "
	#debug("Writing MVgeometryAnalyticsData output file: DONE.")
	#debug("==================================================")
	#debug(" ")
	
	return [midPtTop[0], midPtTop[1], midPtTop[2], annulusRadius]
