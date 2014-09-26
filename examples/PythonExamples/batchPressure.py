import sys
import copy
from lxml import etree     
import os
import ntpath
from path import path



from msml import frontend 
import msml
import msml.env
import msml.model
import msml.run
import msml.xml
import msml.exporter
import msml.exceptions
from msml.exceptions import *


for p in range (5, 80, 5):
    app = frontend.App(exporter='nsofa', output_dir='batchedPressure' + str(p))
    mfile = app._load_msml_file('../CGALi2vLungs/lungs_new.xml')
    mfile.scene[0].constraints[0].constraints[1].pressure = str(p)
    mfile.scene[0].constraints[0].constraints[1].attributes['pressure'] =  str(p)
    mfile.scene[0].constraints[0].constraints[2].pressure =  str(p)
    mfile.scene[0].constraints[0].constraints[2].attributes['pressure'] =  str(p)
    app.execute_msml(mfile)
