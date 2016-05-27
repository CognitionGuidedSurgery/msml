#!C:/Python27/python.exe -W ignore

# Choose the right interpreter above for python dependencies
# given by the requirements of MSML

# This will load the ugly stdout hack and functionalities
# for producing cli xml + argument parsing
import sys
sys.path.append("F:/dev/msml_exp/src")
from msml.api.clisupport import *


# absolute path to MSMLFILE
MSMLFILE = 'F:/dev/msml_exp/examples/CGALi2vExample/CGALExamplePressure.xml'

def main():
    cli_app(MSMLFILE,
        exporter="sofa",
        
        packages = [],
        repositories = [],
        exporter_options= {},
        executor_options = {}
    )

if __name__ == "__main__":
    main()