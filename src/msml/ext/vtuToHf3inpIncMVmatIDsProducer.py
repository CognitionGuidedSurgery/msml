# ======================================================================
# Given 
# - a 3D unstructured grid (vtu file) representation of the MV segmentation 
# (e.g. by CGAL meshing operator, followed by vtk2vtu-Converter), which 
# only contains the connectivity information of 3D cells with four vertices 
# (i.e. tetrahedrons) and no other cells of dimension different from three, 
# and 
# - a 2D polydata surface representation of the MV segmentation, which 
# additionally contains matID-information on the MV leaflets and annulus 
# points, 
# this script produces a hf3-inp-file suitable for a HiFlow3-based 
# MVR-simulation.
# 
# The coordinates of the vertices, the connectivity information of the 
# 3D cells and 2D boundary faces will be written to the hf3-inp-file.
# The matIDs of the cells will be determined as follows:
# - every 3D cell gets the material id 10.
# - surface cells are subdivided into
#   - upside surfaces on anterior leaflet: matID 17,
#   - upside surfaces on posterior leaflet: matID 18,
#   - downside surfaces: matID 20.

# NOTE: The result of this script is NOT DETERMINISTIC! This means that it requires
#       human assessment of the suitability of the results for the simulation algorithm.
# NOTE: This version of the script uses CellNormals (as opposed to PointNormals).
# NOTE: In order to avoid 'blurry' matID-distribution around the interface between
#       between the leaflets (near the commissure points),
#       - either use MITK-remeshing results (2 separate leaflets and 1 complete MV inc IDs),
#       - or possibly use some vtk filter "subdivision" to refine mesh "smoothing"...

# How to run the script:
#   python vtuToHf3inpIncMVmatIDsProducer.py valve3d_volumeMesh.vtu valve2d_SurfaceIncVertexIDs.vtp outputname_hf3.inp

# Author: Nicolai Schoch, EMCL; 2015-04-12.
# ======================================================================

__author__ = 'schoch'
import numpy as np
from numpy import linalg as LA
import sys
import vtk
#from .msmlvtk import * # NEEDED?!
from msml.log import error,info,debug,critical,fatal


def vtu_To_hf3inp_inc_MV_matIDs_Producer(valve3dinputfilename, valve2dinputfilename):
	# ======================================================================
	# Define matIDs --------------------------------------------------------
	ID_UP = 21 # preliminary result, which gets overwritten by ID_ANT and ID_POST.
	ID_DOWN = 20
	ID_ANT = 17
	ID_POST = 18
	
	# ======================================================================
	# get system arguments -------------------------------------------------
	valve3dFilename_ = valve3dinputfilename
	valve2dFilename_ = valve2dinputfilename
	outputFilename_ = "my_cool_hf3inp_outputfilename"
	
	print " "
	print "==========================================================================================="
	print "=== Execute Python script to produce HiFlow3 inp file (incl. matIDs) for MVR-Simulation ==="
	print "==========================================================================================="
	print " "
	#debug(" ")
	#debug("===========================================================================================")
	#debug("=== Execute Python script to produce HiFlow3 inp file (incl. matIDs) for MVR-Simulation ===")
	#debug("===========================================================================================")
	#debug(" ")
	
	# ======================================================================
	# read in files: -------------------------------------------------------
	# read in 3d valve
	# NOTE: ensure that the precedent meshing algorithm (CGAL or similar)
	#       produces consistent/good results w.r.t. the 'normal glyphs'.
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
	
	# compute normals of surface mesh
	normalsSurface_ = vtk.vtkPolyDataNormals()
	if vtk.vtkVersion().GetVTKMajorVersion() >= 6:
  	  normalsSurface_.SetInputData(valve3dSurface_)
	else:
  	  normalsSurface_.SetInput(valve3dSurface_)
	normalsSurface_.SplittingOn()
	normalsSurface_.ConsistencyOn() # such that on a surface the normals are oriented either 'all' outward OR 'all' inward.
	normalsSurface_.AutoOrientNormalsOn() # such that normals point outward or inward.
	normalsSurface_.ComputePointNormalsOff() # adapt here. On/Off.
	normalsSurface_.ComputeCellNormalsOn()   # adapt here.
	normalsSurface_.FlipNormalsOff()
	normalsSurface_.NonManifoldTraversalOn()
	normalsSurface_.Update()
	
	# get cell normals
	normalsSurfaceRetrieved_ = normalsSurface_.GetOutput().GetCellData().GetNormals() # adapt here.
	
	# read in 2d valve -----------------------------------------------------
	vtpreader = vtk.vtkXMLPolyDataReader()
	vtpreader.SetFileName(valve2dFilename_)
	vtpreader.Update()
	valve2d_ = vtpreader.GetOutput()
	
	# compute normals of valve2d_
	normalsValve2d_ = vtk.vtkPolyDataNormals()
	if vtk.vtkVersion().GetVTKMajorVersion() >= 6:
  	  normalsValve2d_.SetInputData(valve2d_)
	else:
  	  normalsValve2d_.SetInput(valve2d_)
	normalsValve2d_.SplittingOn()
	normalsValve2d_.ConsistencyOn()
	normalsValve2d_.ComputePointNormalsOff() # adapt here.
	normalsValve2d_.ComputeCellNormalsOn()
	normalsValve2d_.FlipNormalsOff()
	normalsValve2d_.NonManifoldTraversalOn()
	normalsValve2d_.Update()
	
	# get cell normals
	normalsValve2dRetrieved_ = normalsValve2d_.GetOutput().GetCellData().GetNormals() # adapt here.
	
	print "Reading 3D and 2D-annotated input files: DONE."
	#debug("Reading 3D and 2D-annotated input files: DONE.")
	
	# ======================================================================
	# initialize cell locator for closest cell search ----------------------
	# (using vtk methods, that find the closest point in a grid for an arbitrary point in R^3)
	cellLocator = vtk.vtkCellLocator()
	cellLocator.SetDataSet(valve2d_)
	cellLocator.BuildLocator()
	
	# ======================================================================
	# allocate memory for cell_udlr_list_ (up-down-left-right) -------------
	cell_udlr_list_ = [0 for i in range(valve3dSurface_.GetNumberOfCells())]
	
	# ======================================================================
	# iterate over the cells of the surface and compare normals ------------
	for i in range(valve3dSurface_.GetNumberOfCells()):
  	  # get cellId of closest point
  	  iD = valve3dSurface_.GetCell(i).GetPointId(0) # NOTE: only one (test)point (0) of respective cell
  	  testPoint = valve3dSurface_.GetPoint(iD)
  	  closestPoint = np.zeros(3)
  	  closestPointDist2 = vtk.mutable(0)
  	  cellId = vtk.mutable(0)
  	  subId = vtk.mutable(0)
  	  cellLocator.FindClosestPoint(testPoint, closestPoint, cellId, subId, closestPointDist2)
      
  	  normalSurf_ = np.zeros(3)
  	  normalsSurfaceRetrieved_.GetTuple(i, normalSurf_)
  	  
  	  normalV2d_ = np.zeros(3)
  	  normalsValve2dRetrieved_.GetTuple(cellId, normalV2d_)
  	  
  	  # set cell_udlr_list_ entry to (preliminary) "1", if cell is on upper side of leaflet
  	  if np.dot(normalSurf_, normalV2d_) > 0.0:
  	    cell_udlr_list_[i] = 1 # NOTE: "cell_udlr_list_[i] = 1" means "cell on upside".
  	  
  	# ======================================================================
	# iterate over cells on the upper side of the leaflet surface, and set ids for left/right ------------------
	kDTree = vtk.vtkKdTreePointLocator()
	kDTree.SetDataSet(valve2d_)
	kDTree.BuildLocator()
	
	VertexIDs_ = valve2d_.GetPointData().GetArray('VertexIDs')
	
	# allocate memory for upCellList_ (indicating if cell is on left/right side)
	upCellList_ = [i for i in range(valve3dSurface_.GetNumberOfCells()) if cell_udlr_list_[i]]
	
	for i in upCellList_:
	  iD = valve3dSurface_.GetCell(i).GetPointId(0)
	  testPoint = valve3dSurface_.GetPoint(iD)
	  result_ = vtk.vtkIdList()
	  counter = 1
	  cond_ = True
	  while cond_:
	    kDTree.FindClosestNPoints(counter, testPoint, result_)
	    for j in range(result_.GetNumberOfIds()):
	      iD2 = result_.GetId(j)
	      if int(VertexIDs_.GetTuple1(iD2)) == ID_ANT:
		    cond_ = False
		    cell_udlr_list_[i] = 2 # NOTE: "cell_udlr_list_[i] = 2" means "cell on ANT upside".
	      if int(VertexIDs_.GetTuple1(iD2)) == ID_POST:
		    cond_ = False
		    cell_udlr_list_[i] = 3 # NOTE: "cell_udlr_list_[i] = 3" means "cell on POST upside".
	    counter += 1
	
	print "Computing hf3-inp MV matID information: DONE."
	#debug("Computing hf3-inp MV matID information: DONE.")
	
	# ======================================================================
	# write results to inp file --------------------------------------------
	f = open(outputFilename_, 'w')
	
	# write first line
	s = str(valve3d_.GetNumberOfPoints()) + ' ' + str(valve3dSurface_.GetNumberOfCells()+valve3d_.GetNumberOfCells()) + ' 0 0 0\n'
	f.write(s)
	
	# write point coordinates
	for i in range(valve3d_.GetNumberOfPoints()):
	  pt = valve3d_.GetPoint(i)
	  s = str(i) + ' ' + str(pt[0]) + ' ' + str(pt[1]) + ' ' + str(pt[2]) + '\n'
	  f.write(s)
	
	list_of_facet_matIDints = list()
	
	# write connectivity information of triangles
	# integer, material id, vertex point ids
	for i in range(valve3dSurface_.GetNumberOfCells()):
	  cell = valve3dSurface_.GetCell(i)
	  iDs = cell.GetPointIds()
	  if cell_udlr_list_[i] == 2:     # NOTE: "cell_udlr_list_[i] = 2" means "cell on ANT upside".
	    matId = ID_ANT
	  elif cell_udlr_list_[i] == 3:   # NOTE: "cell_udlr_list_[i] = 3" means "cell on POST upside".
	    matId = ID_POST
	  else:                           # NOTE: "cell_udlr_list_[i] = 0" means "cell on downside".
	    matId = ID_DOWN
	  s = str(0) + ' ' + str(matId) + ' tri ' + str(iDs.GetId(0)) + ' ' + str(iDs.GetId(1)) + ' ' + str(iDs.GetId(2)) + '\n'
	  list_of_matIDints+=[matID, iDs.GetId(0), iDs.GetId(1), iDs.GetId(2)]
	  f.write(s)
	
	list_of_point_matIDints = list()
	
	# write connectivity information of tetrahedrons
	# integer, material id, vertex point ids
	for i in range(valve3d_.GetNumberOfCells()):
	  cell = valve3d_.GetCell(i)
	  iDs = cell.GetPointIds()
	  matId = 10
	  s = str(0) + ' ' + str(matId) + ' tet ' + str(iDs.GetId(0)) + ' ' + str(iDs.GetId(1)) + ' ' + str(iDs.GetId(2)) + ' ' + str(iDs.GetId(3)) + '\n'
	  list_of_point_matIDints+=[10, iDs.GetId(0), iDs.GetId(1), iDs.GetId(2), iDs.GetId(3)]
	  f.write(s)
	
	# close stream
	f.close()
	
	# ======================================================================
	print "Writing HiFlow3 inp output file (incl. MV matIDs): DONE."
	print "========================================================"
	print " "
	#debug("Writing HiFlow3 inp output file (incl. MV matIDs): DONE.")
	#debug("========================================================")
	#debug(" ")
	
	return list_of_matIDints, list_of_point_matIDints
