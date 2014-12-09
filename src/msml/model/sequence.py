# region gplv3preamble
# The Medical Simulation Markup Language (MSML) - Simplifying the biomechanical modeling workflow
#
# MSML has been developed in the framework of 'SFB TRR 125 Cognition-Guided Surgery'
#
# If you use this software in academic work, please cite the paper:
# S. Suwelack, M. Stoll, S. Schalck, N.Schoch, R. Dillmann, R. Bendl, V. Heuveline and S. Speidel,
# The Medical Simulation Markup Language (MSML) - Simplifying the biomechanical modeling workflow,
# Medicine Meets Virtual Reality (MMVR) 2014
#
# Copyright (C) 2013-2014 see Authors.txt
#
# If you have any questions please feel free to contact us at suwelack@kit.edu
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# endregion


__author__ = "Markus Stoll"
__date__ = "2014-09-30"

import glob
import multiprocessing, multiprocessing.pool
from collections import OrderedDict


def executeOperatorSequence(operator, kwargsUpdated, parallel):   
    outputPathPattern = ''
    inputPathPattern = ''
    for key, value in kwargsUpdated.iteritems():
        arg = str(value)
        if '*' in arg:

            if operator.get_targets().count(key) == 1:
                outputPathPattern = arg
                outputKey = key
            else: 
                # get file of path in arg with Unix style pathname pattern expansion
                fileList = glob.glob(arg)
                if not fileList:
                    log.error("%s: Could not find any files for input pattern %s in Slot %s" % operator.name, outputPathPattern, outputKey)
                
                inputFileList = fileList
                inputPathPattern = arg
                inputKey = key

    if outputPathPattern == '' or inputPathPattern == '':
        log.error("If two file patterns (paths with '*' are used, one must be an argument for a non-target parameter and one in target parameter")
            
    pre, post = inputPathPattern.split('*')
    outputFileList = []
    
    for fil in inputFileList:
        tmp = str(fil).replace(pre, '')
        tmp = str(tmp).replace(post, '')  
        outputFileList.append(outputPathPattern.replace('*', tmp))
    
    args_list = []
    for j in range(len(inputFileList)):
        kwargs_new = OrderedDict(kwargsUpdated)
        kwargs_new[inputKey] = inputFileList[j]
        kwargs_new[outputKey] = outputFileList[j]
        args_new = list(kwargs_new.values())
        args_new.append(operator)            
        args_list.append(args_new)
        
    if parallel:
        # multiprocessing
        num_of_workers = multiprocessing.cpu_count()
        pool = multiprocessing.Pool(num_of_workers - 1)
        # blocks until finished
        pool.map(callWrapper, args_list)
    else:
        for args in args_list:
            callWrapper(args)
    return outputPathPattern


import msml.log, os
def callWrapper(selfAndArgs):
    operator = selfAndArgs.pop()
    pid = os.getpid()

    msml.log.info("[PID %d] operator %s , with args: %s" , pid, operator, selfAndArgs)
    tmp =  operator._function(*selfAndArgs)
    msml.log.info("-- finished %d" , pid)

    return tmp
