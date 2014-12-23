import argparse
from msml.cli import get_cli_xml

import msml.log

msml.log.set_verbosity("CRITICAL")

__author__ = 'weigl'

def cliparser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--xml", help="print cli xml", action="store_true")
    return parser

if __name__ == "__main__":


    file = "examples/BunnyExample/bunny.msml.xml"

    p = cliparser()

    ns = p.parse_args()

    if ns.xml:
        print get_cli_xml(file)
    else:
        print "execute bunny xml"