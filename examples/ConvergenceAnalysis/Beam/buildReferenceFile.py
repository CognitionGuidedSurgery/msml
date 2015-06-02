import os
import sys
sys.path.insert(0,"/MedSim2/msml/src") # to use msml imports
import msml.api.simulation_runner as api
import numpy as np
import matplotlib.pyplot as plt

#define reference files
refN = "435606"

# define infiles and output directory
msml_infile_ref = os.path.abspath("beamLinearGravity_reference.msml.xml")
msml_outdir= os.path.abspath("/tmp/MSMLResultsBeamConvergenceAnalysis_buildReference/")


refFile = os.path.abspath("/MedSim2/msml/examples/ConvergenceAnalysis/Beam/Beam_Tet4_NElement={0:s}.vtk".format(refN))
resultRefMeshFile = os.path.abspath(msml_outdir+"/referenceDisp.vtu")

# run reference
myRunner = api.SimulationRunner(msml_infile_ref, "sofa", msml_outdir)
myRunner.update_variable('vol_mesh', refFile)
myRunner.update_variable('resultMesh', resultRefMeshFile)
myRunner.run()