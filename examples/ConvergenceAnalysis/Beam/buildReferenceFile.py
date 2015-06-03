import os
import sys
import msml.envconfig as envconf
sys.path.insert(0,envconf.MSML_ROOT) # to use msml imports
import msml.api.simulation_runner as api
import numpy as np
import matplotlib.pyplot as plt


msmlDir = os.path.abspath(envconf.MSML_ROOT)

#define reference files
refN = "24"

# define infiles and output directory
#msml_infile_ref = os.path.abspath("beamLinearGravity_reference.msml.xml")
msml_infile_ref = os.path.abspath("beamQuadTetsGravity_reference.msml.xml")
msml_outdir= os.path.abspath("/tmp/MSMLResultsBeamConvergenceAnalysis_buildReference/")


refFile = os.path.abspath(msmlDir+"/examples/ConvergenceAnalysis/Beam/Beam_Tet10_NElement={0:s}.vtk".format(refN))
resultRefMeshFile = os.path.abspath(msml_outdir+"/referenceDisp.vtu")

# run reference
myRunner = api.SimulationRunner(msml_infile_ref, "sofa", msml_outdir)
myRunner.update_variable('vol_mesh', refFile)
myRunner.update_variable('resultMesh', resultRefMeshFile)
myRunner.run()