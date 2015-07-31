__author__ = 'dettmann', 'suwelack'
__date__ = "2015-07-24"

import os
import sys
import shutil

from msml.log import debug
import msml.ext.acvd
import msml.ext.tetgen
import msml.ext.misc
import msml.api.simulation_runner as api
import msml.envconfig as envconf

def convertToQuadraticTetra(linearGrid, quadraticGrid, highResSurface):
	# define parameters
	sys.path.insert(0,envconf.MSML_ROOT)
	msmlDir = os.path.abspath(envconf.MSML_ROOT)
	outdir = os.path.abspath("/tmp/MSMLconvertToQuadraticTetra/")
	outfileReducedLinearSurfaceMesh = os.path.abspath(outdir+"/reducedLinearSurfaceMesh.vtk")
	outfileRedLinearVolumeMesh = os.path.abspath(outdir+"/reducedLinearVolumeMesh.vtk")
	outfilequadSurfaceMesh = os.path.abspath(outdir+"/quadSurfaceMesh.vtk")
	outfileProjection = os.path.abspath(outdir+"/meshProjection.vtk")
	outfileResultMesh = os.path.abspath(outdir+"/resultQuadraticMesh.vtk")

	# create temporary output folder
	if not os.path.exists(outdir):
		os.makedirs(outdir)

	# workflow
	msml.ext.acvd.ReduceSurfaceMesh(linearGrid, outfileReducedLinearSurfaceMesh, highResSurface, False, True)
	msml.ext.tetgen.TetgenCreateVolumeMesh(outfileReducedLinearSurfaceMesh, outfileRedLinearVolumeMesh, False, 1.4, 0, 0, 2, True, True, True)
	msml.ext.misc.ConvertLinearToQuadraticTetrahedralMeshPython(outfileRedLinearVolumeMesh, outfilequadSurfaceMesh)
	projected = msml.ext.misc.ProjectVolumeMeshDisp(outfilequadSurfaceMesh, outfileProjection, linearGrid)

	# get quadratic tetrahedral mesh with displacement vector
	myRunner = api.SimulationRunner(os.path.abspath(msmlDir+"/src/msml/ext/getQuadMeshWithDistance.xml"), "sofa", outdir)
	myRunner.update_variable('vol_mesh', outfilequadSurfaceMesh)
	myRunner.update_variable('dispVar', projected.displacements)
	myRunner.update_variable('surfacePointsIds', projected.surfacePointsIds)
	myRunner.update_variable('resultMesh', outfileResultMesh)
	myRunner.run()

	# copy result to variable
	msml.ext.misc_python.copy_file(outfileResultMesh, quadraticGrid, False)

	# remove temporary output folder
	shutil.rmtree(outdir)