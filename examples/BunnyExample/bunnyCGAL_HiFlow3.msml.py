#!/usr/bin/python -W ignore

# Choose the right interpreter above for python dependencies
# given by the requirements of MSML

# This will load the ugly stdout hack and functionalities
# for producing cli xml + argument parsing
import sys
sys.path.append("/home/nschoch/Workspace/MSML/msml/src")
from msml.api.clisupport import *


# absolute path to MSMLFILE
MSMLFILE = '/home/nschoch/Workspace/MSML/msml/examples/BunnyExample/bunnyCGAL_HiFlow3.msml.xml'

def main():
    cli_app(MSMLFILE,
        exporter="hiflow3",
        
        packages = [],
        repositories = [],
        exporter_options= {},
        executor_options = {}
    )

if __name__ == "__main__":
    main()