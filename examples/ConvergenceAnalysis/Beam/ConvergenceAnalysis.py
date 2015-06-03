import os
import sys
import msml.envconfig as envconf
sys.path.insert(0,envconf.MSML_ROOT) # to use msml imports
import msml.api.simulation_runner as api
import numpy as np
import matplotlib.pyplot as plt

# define pathes
msmlDir = os.path.abspath(envconf.MSML_ROOT)
msml_outdir= os.path.abspath("/tmp/MSMLResultsBeamConvergenceAnalysis/")

# define infiles and output directory
msml_infile_ref = os.path.abspath("beamLinearGravity_reference.msml.xml")
msml_infile_test = os.path.abspath("beamLinearGravity_test.msml.xml")

#define reference files
refN = "435606"
testN = ["371","712","1810","4621","8990","19128","45418"]
noNodes =["131, 225,487, 1074, 1996,3994,9071"]
refFile = os.path.abspath(msmlDir+"/examples/ConvergenceAnalysis/Beam/Beam_Tet4_NElement={0:s}.vtk".format(refN))
resultRefMeshFile = os.path.abspath(msmlDir+"/examples/ConvergenceAnalysis/Beam/referenceDisp_Tet4_NElement=435606.vtu")

# run test sessions and compute mean error
allMeanError = []
for i in testN:
    testFile = os.path.abspath(msmlDir+"/examples/ConvergenceAnalysis/Beam/Beam_Tet4_NElement={0:s}.vtk".format(i))
    resultTestMeshFile = os.path.abspath(msml_outdir+"/test{0:s}Disp.vtu".format(i))
    resultTransformTestMeshFile = os.path.abspath(msml_outdir+"/test{0:s}TransformMesh.vtk".format(i))

    #run test file
    myRunner = api.SimulationRunner(msml_infile_test, "sofa", msml_outdir)
    myRunner.update_variable('vol_mesh', testFile)
    myRunner.update_variable('resultMesh', resultTestMeshFile)
    myRunner.update_variable('vol_mesh_ref', refFile)
    myRunner.update_variable('resultTransformMesh', resultTransformTestMeshFile)
    myRunner.update_variable('outputRef', resultRefMeshFile)
    myRunner.run()

    #get mean error
    allMeanError.append(myRunner.get_results('meanError', 'error'))

print("MeanError:" + str(allMeanError))

#plot
print("Start plotting...")
plt.loglog(noNodes, allMeanError, 'ro')
plt.xlabel('NNodes')
plt.ylabel('Root Mean Square')
plt.title('Convergence Analysis')
plt.show()
