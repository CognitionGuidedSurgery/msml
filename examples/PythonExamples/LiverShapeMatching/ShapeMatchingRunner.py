__author__ = 'Stefan Suwelack'
import imp, sys

import os
import msml.api.simulation_runner as api


#create one forward simulation

msml_file = os.path.abspath('LiverShapeMatching.msml.xml')

#myRunner = api.SimulationRunner(msml_file, "sofa", "/homes/staff/suwelack/MedicalPhysics/MSML/Results")
myRunner = api.SimulationRunner(msml_file, "sofa", "/tmp/MSMLResultsLiverShapeMatching")

myRunner.run()


