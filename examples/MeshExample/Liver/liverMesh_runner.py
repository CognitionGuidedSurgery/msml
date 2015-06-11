import os
import sys
import msml.envconfig as envconf
sys.path.insert(0,envconf.MSML_ROOT) # to use msml imports
import msml.api.simulation_runner as api
import msml.ext.misc

# define pathes
msmlDir = os.path.abspath(envconf.MSML_ROOT)
msml_infile_test = os.path.abspath(msmlDir+"/examples/MeshExample/Liver/liverReduce.xml")
msml_outdir = os.path.abspath("/tmp/MSMLResultsLiverMesh/")

#define parameters
###################################
noVertices = "1800"
maxEdgeRadiusRatio = "1.4"
###################################
infile_mesh = os.path.abspath(msmlDir+"/examples/MeshExample/Liver/HELP_Liver_Segmented.vtk")
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

# test mesh quality
measure_names = ["EdgeRatio", "Volume", "MinAngle"]
quality_results = msml.ext.misc.MeasureTetrahedricMeshQuality(outfileVolumeMesh, measure_names)

for q in quality_results:
    print("Mesh quality measure: " + str(q.qualityMeasureName))
    print("min: " + str(q.min))
    print("max: " + str(q.max))
    print("avg: " + str(q.avg))
    print("var: " + str(q.var))
    print("n: " + str(q.n))