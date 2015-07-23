import os
import sys
import msml.envconfig as envconf
import msml.api.simulation_runner as api

# to use msml imports
sys.path.insert(0,envconf.MSML_ROOT)

################# define pathes and parameters ###############################################################################
msmlDir = os.path.abspath(envconf.MSML_ROOT)
msml_infile_first = os.path.abspath(msmlDir+"/examples/MeshExample/Tet10/tet10.xml")
msml_infile_second = os.path.abspath(msmlDir+"/examples/MeshExample/Tet10/adaptTet10.xml")
msml_outdir = os.path.abspath("/tmp/MSMLResultsTet10/")
# reference mesh
infile_mesh = os.path.abspath(msmlDir+"/examples/MeshExample/Tet10/IRACD_liver_5.vtk")
# reduce mesh
noVertices = "100" #default: 1800
maxEdgeRadiusRatio = "1.4" #default: 1.4
outfileReduceMesh = os.path.abspath(msml_outdir+"/liverReduced{0:s}.vtk".format(noVertices))
# create volume mesh linear
outfileLinVolumeMesh = os.path.abspath(msml_outdir+"/liverLinVolume{0:s}_maxEdge{1:s}.vtk".format(noVertices, maxEdgeRadiusRatio))
# create quadratic tetrahedral mesh
outfileQuadVolumeMesh = os.path.abspath(msml_outdir+"/liverQuadVolume{0:s}_maxEdge{1:s}.vtk".format(noVertices, maxEdgeRadiusRatio))
outfileProjection = os.path.abspath(msml_outdir+"/liverProjection_Volume{0:s}_maxEdge{1:s}.vtk".format(noVertices, maxEdgeRadiusRatio))
outfileResultMesh = os.path.abspath(msml_outdir+"/liverResultMesh_Volume{0:s}_maxEdge{1:s}.vtk".format(noVertices, maxEdgeRadiusRatio))

################# run first simulation  #######################################################################################
# reduce reference mesh
# create linear volume mesh
# create quadratic tetrahedral surface
myRunner = api.SimulationRunner(msml_infile_first, "sofa", msml_outdir)
myRunner.update_variable('refVolumeMesh', infile_mesh)
myRunner.update_variable('redVerticesCount', noVertices)
myRunner.update_variable('redMaxEdgeRadiusRatio', maxEdgeRadiusRatio)
myRunner.update_variable('outputReduceMesh', outfileReduceMesh)
myRunner.update_variable('outputLinVolumeMesh', outfileLinVolumeMesh)
myRunner.update_variable('outputQuadVolumeMesh', outfileQuadVolumeMesh)
myRunner.update_variable('outputProjection', outfileProjection)
myRunner.run()
# get displacement vector and surface point ids
projected = myRunner.get_results('projection', 'ResultProjection')

################# run second simulation  #######################################################################################
# get quadratic tetrahedral mesh with displacement vector
myRunner2 = api.SimulationRunner(msml_infile_second, "sofa", msml_outdir)
myRunner2.update_variable('vol_mesh', outfileQuadVolumeMesh)
myRunner2.update_variable('dispVar', projected.displacements)
myRunner2.update_variable('surfacePointsIds', projected.surfacePointsIds)
myRunner2.update_variable('resultMesh', outfileResultMesh)
myRunner2.run()
