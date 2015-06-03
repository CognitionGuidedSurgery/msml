import os
import sys
import msml.envconfig as envconf
sys.path.insert(0,envconf.MSML_ROOT) # to use msml imports
import msml.api.simulation_runner as api
import numpy as np
import matplotlib.pyplot as plt

# define pathes
msmlDir = os.path.abspath(envconf.MSML_ROOT)
msml_infile_test = os.path.abspath(msmlDir+"/examples/MeshExample/Liver/liverReduce.xml")
msml_outdir = os.path.abspath("/tmp/MSMLResultsLiverMesh/")

#define parameters
noVertices = "1800"
maxEdgeRadiusRatio = "1.4"
infile_mesh = os.path.abspath(msmlDir+"/examples/MeshExample/Liver/IRACD_liver_5.vtk")
outfileReduceMesh = os.path.abspath(msml_outdir+"/liverReduced{0:s}.vtk".format(noVertices))
outfileVolumeMesh = os.path.abspath(msml_outdir+"/liverSmallVolume{0:s}_maxEdge{1:s}.vtk".format(noVertices, maxEdgeRadiusRatio))

#run file
myRunner = api.SimulationRunner(msml_infile_test, "sofa", msml_outdir)
myRunner.update_variable('vol_mesh', infile_mesh)
myRunner.update_variable('redVerticesCount', noVertices)
myRunner.update_variable('redMaxEdgeRadiusRatio', maxEdgeRadiusRatio)
myRunner.update_variable('outputReduceMesh', outfileReduceMesh)
myRunner.update_variable('outputMeshFile', outfileVolumeMesh)
myRunner.run()