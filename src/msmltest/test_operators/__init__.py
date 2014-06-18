__author__ = 'weigl'

import msml.log

def report(level, message, variable):
    msml.log.report(message+str(variable), kind=level)
