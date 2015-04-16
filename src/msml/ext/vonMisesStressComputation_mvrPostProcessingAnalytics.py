# ======================================================================
# Given vtu/pvtu file(s) resulting from an MVR elasticity simulation 
# (the solution files hence contain three scalar valued arrays named 
# 'u0', 'u1' and 'u2' as PointData), this vtk-based python script
# warps the initial/original mesh geometry by means of the displacement
# vector, and computes the Cauchy strain tensor and the von Mises stress.
# 
# The script's output is the following:
#  - vtu file that contains all the data of the
#    original file with modified coordinates of the points and the 
#    displacement vector as additional PointData and the strain tensor 
#    along with the von Mises stress (w.r.t. the Lame parameters 
#    lambda = 28466, mu = 700 for mitral valve tissue, according to 
#    [Mansi-2012]) as additional CellData.
# 
# How to run the script:
#   python calculator.py ./input/myInput.(p)vtu ./output/myOutput.vtu
# 
# Author: Nicolai Schoch, EMCL; 2015-04-12.
# ======================================================================

__author__ = 'schoch'
import sys
import vtk
#from .msmlvtk import * # NEEDED?!


def compute_vonMisesStress_for_MV(inputfilename, outputfilename):
	# ======================================================================
	# get system arguments -------------------------------------------------
	# Path to input file and name of the output file
	#inputfilename = sys.argv[1]
	#outputfilename = sys.argv[2]
	
	print " "
	print "=================================================================================================="
	print "=== Execute Python script to analyze MV geometry in order for the HiFlow3-based MVR-Simulation ==="
	print "=================================================================================================="
	print " "
	
	# ======================================================================
	# Read file
	if inputfilename[-4] == 'p':
		reader = vtk.vtkXMLPUnstructuredGridReader()
		reader.SetFileName(inputfilename)
		reader.Update()
	else:
		reader = vtk.vtkXMLUnstructuredGridReader()
		reader.SetFileName(inputfilename)
		reader.Update()
	
	print "Reading input files: DONE."
	
	# ======================================================================
	# Compute displacement vector
	calc = vtk.vtkArrayCalculator()
	calc.SetInput(reader.GetOutput())
	calc.SetAttributeModeToUsePointData()
	calc.AddScalarVariable('x', 'u0', 0)
	calc.AddScalarVariable('y', 'u1', 0)
	calc.AddScalarVariable('z', 'u2', 0)
	calc.SetFunction('x*iHat+y*jHat+z*kHat')
	calc.SetResultArrayName('DisplacementSolutionVector')
	calc.Update()
	
	# ======================================================================
	# Compute strain tensor
	derivative = vtk.vtkCellDerivatives()
	derivative.SetInput(calc.GetOutput())
	derivative.SetTensorModeToComputeStrain()
	derivative.Update()
	
	# ======================================================================
	# Compute von Mises stress
	calc = vtk.vtkArrayCalculator()
	calc.SetInput(derivative.GetOutput())
	calc.SetAttributeModeToUseCellData()
	calc.AddScalarVariable('Strain_0', 'Strain', 0)
	calc.AddScalarVariable('Strain_1', 'Strain', 1)
	calc.AddScalarVariable('Strain_2', 'Strain', 2)
	calc.AddScalarVariable('Strain_3', 'Strain', 3)
	calc.AddScalarVariable('Strain_4', 'Strain', 4)
	calc.AddScalarVariable('Strain_5', 'Strain', 5)
	calc.AddScalarVariable('Strain_6', 'Strain', 6)
	calc.AddScalarVariable('Strain_7', 'Strain', 7)
	calc.AddScalarVariable('Strain_8', 'Strain', 8)
	calc.SetFunction('sqrt( (2*700*Strain_0 + 28466*(Strain_0+Strain_4+Strain_8))^2 + (2*700*Strain_4 + 28466*(Strain_0+Strain_4+Strain_8))^2 + (2*700*Strain_8 + 28466*(Strain_0+Strain_4+Strain_8))^2 - ( (2*700*Strain_0 + 28466*(Strain_0+Strain_4+Strain_8))*(2*700*Strain_4 + 28466*(Strain_0+Strain_4+Strain_8)) ) - ( (2*700*Strain_0 + 28466*(Strain_0+Strain_4+Strain_8))*(2*700*Strain_8 + 28466*(Strain_0+Strain_4+Strain_8)) ) - ( (2*700*Strain_4 + 28466*(Strain_0+Strain_4+Strain_8))*(2*700*Strain_8 + 28466*(Strain_0+Strain_4+Strain_8)) ) + 3 * ((2*700*Strain_3)^2 + (2*700*Strain_6)^2 + (2*700*Strain_7)^2) )')
	calc.SetResultArrayName('vonMisesStress_forMV_mu700_lambda28466')
	calc.Update()
	
	print "Computation of displacement vectors, Cauchy strain and vom Mises stress: DONE."
	
	# ======================================================================
	# Define dummy variable; get output of calc filter
	dummy = calc.GetOutput()
	
	# Get point data arrays u0, u1 and u2
	pointData_u0 = dummy.GetPointData().GetArray('u0')
	pointData_u1 = dummy.GetPointData().GetArray('u1')
	pointData_u2 = dummy.GetPointData().GetArray('u2')
	
	# Set scalars
	dummy.GetPointData().SetScalars(pointData_u0)
	
	# ======================================================================
	# Warp by scalar u0
	warpScalar = vtk.vtkWarpScalar()
	warpScalar.SetInput(dummy)
	warpScalar.SetNormal(1.0,0.0,0.0)
	warpScalar.SetScaleFactor(1.0)
	warpScalar.SetUseNormal(1)
	warpScalar.Update()
	
	# Get output and set scalars
	dummy = warpScalar.GetOutput()
	dummy.GetPointData().SetScalars(pointData_u1)
	
	# ======================================================================
	# Warp by scalar u1
	warpScalar = vtk.vtkWarpScalar()
	warpScalar.SetInput(dummy)
	warpScalar.SetNormal(0.0,1.0,0.0)
	warpScalar.SetScaleFactor(1.0)
	warpScalar.SetUseNormal(1)
	warpScalar.Update()
	
	# Get output and set scalars
	dummy = warpScalar.GetOutput()
	dummy.GetPointData().SetScalars(pointData_u2)
	
	# ======================================================================
	# Warp by scalar u2
	warpScalar = vtk.vtkWarpScalar()
	warpScalar.SetInput(dummy)
	warpScalar.SetNormal(0.0,0.0,1.0)
	warpScalar.SetScaleFactor(1.0)
	warpScalar.SetUseNormal(1)
	warpScalar.Update()
	
	# Get ouput and add point data arrays that got deleted earlier
	dummy = warpScalar.GetOutput()
	dummy.GetPointData().AddArray(pointData_u0)
	dummy.GetPointData().AddArray(pointData_u1)
	
	# ======================================================================
	# Write output to vtu
	writer = vtk.vtkXMLUnstructuredGridWriter()
	writer.SetDataModeToAscii()
	writer.SetFileName(outputfilename)
	writer.SetInput(dummy)
	writer.Write()
	
	# ======================================================================
	print "Writing Extended VTU incl. von Mises Stress information: DONE."
	print "=============================================================="
	print " "
