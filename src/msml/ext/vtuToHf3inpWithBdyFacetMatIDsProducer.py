# ======================================================================
# Given an unstructured grid (vtu file), which only contains the 
# connectivity information of 3D cells with four vertices (i.e. 
# tetrahedrons) and no other cells of dimension different from three, 
# this script computes the cell normals of the 2D boundary faces of the 
# mesh. 
# The coordinates of the vertices, the connectivity information of the 
# 3D cells and 2D boundary faces will be written to an inp file. The 
# material id of the cells will be determined as follows:
# - every 3D cell gets the material id 10.
# - if the z-coordinate of the boundary face's normal is greater than 
# zero, the corresponding 2D cell gets the material id 30,
# - otherwise its material id will be 20.

# How to run the script:
#   python vtuToHf3inpWithBdyFacetMatIDsProducer.py inputfilename.vtu <Integer>

# If no3Integer == 0 then the script writes the connectivity information
# of the tetrahedrons to the inp file. Otherwise it will write no 
# information about 3D cells.
# The default value is 0 and one does not have to pass the argument.

# Output:
#   inputfilename.inp

# Author: Nicolai Schoch, EMCL; 2014-12-10.
# ======================================================================

__author__ = 'schoch'
import sys
import vtk
#from .msmlvtk import * # NEW 2014-12-23


def vtu_To_Hf3inpWithBdyFacetMatID_Producer(inputfilename, outputfilename, integer):
	# ======================================================================
	# Define material ids
	# ======================================================================
	ID_TET = 10
	ID_FACET_UP_LEFT = 31
	ID_FACET_UP_RIGHT = 32
	ID_FACET_BELOW = 20
	
	print " "
	print "========================================================="
	print "=== Execute Python script to produce HiFlow3 inp file ==="
	print "========================================================="
	print " "
	
	# ======================================================================
	# Define separating hyperplane with normal n
	# x0 is an element of the plane
	# ======================================================================
	n = [1.0, -0.05, 0.5]
	x0 = [85.35, 93.7, 105.8] 
	
	# ======================================================================
	# Get the name of the vtu file and set value for variable 'no3DCells'.
	# If no3DCells == 0 then the script writes the connectivity information
	# of the tetrahedrons to the inp file. Otherwise it will write no 
	# information about 3D cells.
	# ======================================================================
	#inputfilename = sys.argv[1]
	
	#if len(sys.argv) > 2:
	#  no3DCells = sys.argv[2]
	#else:
	#  no3DCells = 0
	no3DCells = 0
	
	# ======================================================================
	# Create an object of the class 'vtkXMLUnstructuredGridReader'.
	# Read in the vtu file, update the reader and get its output.
	# ======================================================================
	reader = vtk.vtkXMLUnstructuredGridReader()
	reader.SetFileName(inputfilename)
	reader.Update()
	unstructuredGrid = reader.GetOutput()
	# Alternatively:
	#unstructuredGrid = read_ugrid(inputfilename) # NEW 2014-12-23
	print "Reading vtu input file: DONE."
	print "Executing script ..."
	
	# ======================================================================
	# Use 'vtkGeometryFilter' to extract 2D faces on the boundary of 
	# 'unstructuredGrid'.
	# Update the filter and get its output, which is of type 'vtkPolyData'.
	# ======================================================================
	geometryFilter = vtk.vtkGeometryFilter()
	version = vtk.vtkVersion()
	
	if version.GetVTKMajorVersion() >= 6:
		geometryFilter.SetInputData(unstructuredGrid)
	else:
		geometryFilter.SetInput(unstructuredGrid)
	
	geometryFilter.Update()
	boundaryFaces = geometryFilter.GetOutput()
	
	# ======================================================================
	# Create 'vtkPolyDataNormals' object in order to compute normals of
	# boundary faces. Set ComputePointNormals to 'off' and
	# ComputeCellNormals to 'on'. Update the filter.
	# ======================================================================
	normals = vtk.vtkPolyDataNormals()
	
	if version.GetVTKMajorVersion() >= 6:
		normals.SetInputData(boundaryFaces)
	else:
		normals.SetInput(boundaryFaces)
		
	normals.ComputePointNormalsOff()
	normals.ComputeCellNormalsOn()
	normals.Update()
	
	# ======================================================================
	# Retrieve array of normals of boundary cells and add data to
	# the polygonal mesh 'boundaryFaces'.
	# ======================================================================
	cellNormalArray = normals.GetOutput().GetCellData().GetNormals()
	boundaryFaces.GetCellData().SetNormals(cellNormalArray)
	
	# ======================================================================
	# Create inp file with the following content:
	# - coordinates of the vertices of the unstructured grid
	# - connectivity information of the 3D cells of the unstructured grid
	# - connectivity information of the 2D cells of the polygonal mesh
	# The file's name will be the name of the input file with the 
	# appropriate ending.
	# ======================================================================
	#outputfilename = inputfilename[0:len(inputfilename)-3] + 'inp'
	f = open (outputfilename, 'w')
	# Write first line, i.e. total number of vertices, total number of cells and three times 0.
	if no3DCells == 0:
		print >> f, unstructuredGrid.GetNumberOfPoints(),\
		  boundaryFaces.GetNumberOfCells()+unstructuredGrid.GetNumberOfCells(),\
		  0, 0, 0
	else:
		print >> f, unstructuredGrid.GetNumberOfPoints(),\
	      boundaryFaces.GetNumberOfCells(), 0, 0, 0
	
	# Write coordinates of vertices.
	for i in range (0, unstructuredGrid.GetNumberOfPoints()):
		point = unstructuredGrid.GetPoint(i)
		print >> f, i, point[0], point[1], point[2]
	
	# Write connectivity information of tetrahedrons, which are the 3D cells of the unstructured grid.
	if no3DCells == 0:
		for i in range (0, unstructuredGrid.GetNumberOfCells()):
			cellPointIds = unstructuredGrid.GetCell(i).GetPointIds()
			cellPointIdsString = ''
			for j in range (0, cellPointIds.GetNumberOfIds()):
				cellPointIdsString += str(cellPointIds.GetId(j)) + ' '
			print >> f, i, ID_TET, 'tet', cellPointIdsString
	
	# Write connectivity information of triangles, which are the 2D cells of the polygonal mesh.
	cellNormalsRetrieved = boundaryFaces.GetCellData().GetNormals()
	for i in range (0, boundaryFaces.GetNumberOfCells()):
		cellNormal = cellNormalsRetrieved.GetTuple(i)
		cellPointIds = boundaryFaces.GetCell(i).GetPointIds()
		cellPointIdsString = ''
		for j in range (0, cellPointIds.GetNumberOfIds()):
			cellPointIdsString += str(cellPointIds.GetId(j)) + ' '
		# Set material id w.r.t. z-coordinate of normal vector
		material_id = ID_FACET_BELOW
		if cellNormal[2] > 0:
			material_id = ID_FACET_UP_RIGHT
			point = boundaryFaces.GetPoint(cellPointIds.GetId(0))
			if n[0]*(point[0]-x0[0])+n[1]*(point[1]-x0[1])+n[2]*(point[2]-x0[2]) < 0:
				material_id = ID_FACET_UP_LEFT
		print >> f, i, material_id, 'tri', cellPointIdsString
	# Close stream
	f.close()
	
	print "Writing HiFlow3 inp output file (including MaterialNumbers for boundaryFaces): DONE."
	print "========================================================="
	print " "
