__author__ = 'suwelack'
from shutil import copyfile
import os

def copy_file(filename_in, filename_out, workingdir):
    #test if filename_out has no pathname, if s
    #print

    #print(filename_out)
    if(workingdir):
        filename_out = os.path.basename(filename_out)

    copyfile(filename_in, filename_out)
    #print(filename_in)
    #print(filename_out)