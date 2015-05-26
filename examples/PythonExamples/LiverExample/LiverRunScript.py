import os
import sys
sys.path.insert(0,"/opt/msml/src") # to use msml imports
import msml.api.simulation_runner as api

msml_infile = os.path.abspath("liverLinear.msml.xml")
msml_outdir = os.path.abspath("/tmp/MSMLResultsLiver/")

myRunner = api.SimulationRunner(msml_infile, "sofa", msml_outdir)
myRunner.run()