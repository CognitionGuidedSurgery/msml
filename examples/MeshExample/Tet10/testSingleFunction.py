import os
import sys
import msml.envconfig as envconf
import msml.api.simulation_runner as api
import msml.ext.quadTetConverter

# to use msml imports
sys.path.insert(0,envconf.MSML_ROOT)
msmlDir = os.path.abspath(envconf.MSML_ROOT)

# define parameters
infile = os.path.abspath(msmlDir+"/examples/MeshExample/Tet10/IRACD_liver_5.vtk")

msml_outdir_xml = os.path.abspath("/tmp/MSMLTet10_XML/")
msml_outdir_python =os.path.abspath("/tmp/MSMLTet10_Python/")

outfile_xml = os.path.abspath(msml_outdir_xml+"/resultQuadMesh.vtk")
outfile_python = os.path.abspath(msml_outdir_python+"/resultQuadMesh.vtk")

# run simulation
myRunner = api.SimulationRunner("testSingleConversion.xml", "sofa", msml_outdir_xml)
myRunner.update_variable('linVolumeMesh', infile)
myRunner.update_variable('quadVolumeMesh', outfile_xml)
myRunner.run()

# run python method
if not os.path.exists(msml_outdir_python):
    os.makedirs(msml_outdir_python)
msml.ext.quadTetConverter.convertToQuadraticTetra(infile, outfile_python, 100)