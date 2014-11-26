__author__ = 'Stefan Suwelack'
import imp, sys

import os
import msml.api.simulation_runner as api


#create one forward simulation

msml_file = os.path.abspath('beamLinearDisp.msml.xml')

myRunner = api.SimulationRunner(msml_file, "sofa", "/tmp/MSMLResults/")
myRunner.update_variable('dispVar', [0,0,1.0])
myRunner.run()
referencePoints = myRunner.get_results('finalPointDisp', 'points')

