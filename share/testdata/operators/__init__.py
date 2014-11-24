__author__ = 'weigl'

import msml.log

def report(level, message, variable):
    msml.log.info(str(message)+str(variable))
