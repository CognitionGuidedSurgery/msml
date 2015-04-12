# ======================================================================
# Given the following input data w.r.t. a mitral valve setup:
# - a 3D volume mesh (vtu), 
# - a 2D surface mesh representation of the MV segmentation (vtp), and 
# - an Annuloplasty Ring representation including vertex IDs (vtp) 
# this script computes and sets the Dirichlet Boundary Conditions (BCs) 
# data for the HiFlow3-based MVR-Simulation.
# 
# NOTE: Adding additional BC-points by means of linear interpolation
# requires the input IDs to be ordered and going around annulus once!!!
# 
# How to run the script:
#   python script.py valve3d.vtu valve2d.vtp ring.vtp outputname.xml
# 
# Author: Nicolai Schoch, EMCL; 2015-04-12.
# ======================================================================

__author__ = 'schoch'
import numpy as np
from numpy import linalg as LA
import sys
import vtk
import xml.etree.ElementTree as ET # NEEDED?!
#from .msmlvtk import * # NEEDED?!


def BCdata_for_Hf3Sim_Producer(inputfilename, surfaceMesh, ringFilename, outputfilename):
	# ======================================================================
	# define number of given annulus point IDs -----------------------------
	# (see notation/representation of Annuloplasty Rings by DKFZ and corresponding addInfo)
	numberOfAnnulusPtIDs_ = 16
	
	# get system arguments -------------------------------------------------
	valve3dFilename_ = inputfilename
	valve2dFilename_ = surfaceMesh
	ringFilename_ = ringFilename
	outputFilename_ = outputfilename
	
	print " "
	print "====================================================================================="
	print "=== Execute Python script to produce BCdata for the  HiFlow3-based MVR-Simulation ==="
	print "====================================================================================="
	print " "
	
	# ======================================================================
	# read in files: -------------------------------------------------------
	# read in 3d valve
	vtureader = vtk.vtkXMLUnstructuredGridReader()
	vtureader.SetFileName(valve3dFilename_)
	vtureader.Update()
	valve3d_ = vtureader.GetOutput()
	
	# get surface mesh of valve3d_
	geometryFilter = vtk.vtkGeometryFilter()
	if vtk.vtkVersion().GetVTKMajorVersion() >= 6:
		geometryFilter.SetInputData(valve3d_)
	else:
		geometryFilter.SetInput(valve3d_)
	geometryFilter.Update()
	valve3dSurface_ = geometryFilter.GetOutput()
	
	# read in 2d valve
	vtpreader = vtk.vtkXMLPolyDataReader()
	vtpreader.SetFileName(valve2dFilename_)
	vtpreader.Update()
	valve2d_ = vtpreader.GetOutput()
	
	# read in ring
	vtpreader = vtk.vtkXMLPolyDataReader()
	vtpreader.SetFileName(ringFilename_)
	vtpreader.Update()
	ring_ = vtpreader.GetOutput()
	
	# get vertex ids of valve2d_ and ring_ ---------------------------------
	valve2dVertexIds_ = valve2d_.GetPointData().GetArray('VertexIDs')
	ringVertexIds_ = ring_.GetPointData().GetArray('VertexIDs')
	
	print "Reading input files: DONE."
	
	# ======================================================================
	# init. tree for closest point search ----------------------------------
	kDTree = vtk.vtkKdTreePointLocator()
	kDTree.SetDataSet(valve3dSurface_)
	kDTree.BuildLocator()
	
	# ======================================================================
	# arrays for storage of coordinates of annulus points (and interpolated points) on the MV surface and on the ring -----------------
	ringPoints_ = np.zeros((2*numberOfAnnulusPtIDs_,3))
	valvePoints_ = np.zeros((2*numberOfAnnulusPtIDs_,3))
	
	# Store coordiantes in arrays ---------------------------------------------------------------------------
	# NOTE: Wenn korrekte Daten von DKFZ vorhanden, dann kann man auch die Arrays VertexIDs durchlaufen und nur die point id speichern ???????
	# find coordinates of points of ring_
	for i in range(ring_.GetNumberOfPoints()):
		if 0 <= int(ringVertexIds_.GetTuple1(i)) and int(ringVertexIds_.GetTuple1(i)) < numberOfAnnulusPtIDs_:
			ringPoints_[int(ringVertexIds_.GetTuple1(i))] = np.array(ring_.GetPoint(i))
	
	# find coordinates of points of valve2d_
	for i in range(valve2d_.GetNumberOfPoints()):
		if 0 <= int(valve2dVertexIds_.GetTuple1(i)) and int(valve2dVertexIds_.GetTuple1(i)) < numberOfAnnulusPtIDs_:
			valvePoints_[int(valve2dVertexIds_.GetTuple1(i))] = np.array(valve2d_.GetPoint(i))
	
	# find closest points to points stored in valvePoints_ on valve3dSurface_ and store (i.e. overwrite) them in valvePoints_
	for i in range(numberOfAnnulusPtIDs_):
		iD = kDTree.FindClosestPoint(valvePoints_[i])
		kDTree.GetDataSet().GetPoint(iD, valvePoints_[i])
	
	# ======================================================================
	# add additional boundary conditions by linear interpolation -------------------------------------------
	# NOTE: this requires the IDs to be ordered and going around annulus once!!!
	for i in range(numberOfAnnulusPtIDs_):
		valvePoints_[numberOfAnnulusPtIDs_+i] = 0.5 * (valvePoints_[i]+valvePoints_[(i+1)%numberOfAnnulusPtIDs_])
		ringPoints_[numberOfAnnulusPtIDs_+i] = 0.5 * (ringPoints_[i]+ringPoints_[(i+1)%numberOfAnnulusPtIDs_])
	
	# ======================================================================
	# Compute displacements ------------------------------------------------
	displacement_ = ringPoints_ - valvePoints_
	
	# ======================================================================
	# convert arrays to strings --------------------------------------------
	valvePointString_ = ""
	displacementString_ = ""
	for i in range(2*numberOfAnnulusPtIDs_):
		for j in range(3):
			valvePointString_ += str(valvePoints_[i][j])
			displacementString_ += str(displacement_[i][j])
			if j == 2:
				if i < 2*numberOfAnnulusPtIDs_-1:
					valvePointString_ += ";"
					displacementString_ += ";"
			else:
				valvePointString_ += ","
				displacementString_ += ","
	
	print "Computing BC data: DONE."
	
	# ======================================================================
	# Write BC data to XML file --------------------------------------------
	# build a tree structure
	root = ET.Element("Param")
	BCData = ET.SubElement(root, "BCData")
	DisplacementConstraintsBCs = ET.SubElement(BCData, "DisplacementConstraintsBCs")
	
	numberOfDPoints = ET.SubElement(DisplacementConstraintsBCs, "NumberOfDisplacedDirichletPoints")
	numberOfDPoints.text = str(2*numberOfAnnulusPtIDs_)
	
	dDPoints = ET.SubElement(DisplacementConstraintsBCs, "dDPoints")
	dDPoints.text = valvePointString_
	
	dDisplacements = ET.SubElement(DisplacementConstraintsBCs, "dDisplacements")
	dDisplacements.text = displacementString_
	
	# wrap it in an ElementTree instance, and save as XML
	tree = ET.ElementTree(root)
	tree.write(outputFilename_)
	
	# ======================================================================
	print "Writing mvrSimBCdata.xml output file: DONE."
	print "==========================================="
	print " "
