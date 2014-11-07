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


def executeOperatorSequence(operator, args, parallel):
    count = sum('*' in str(arg) for arg in args)
    if count == 2:
        outputPathPattern = ''
        inputPathPattern = ''
        for i, arg in enumerate(args):
            arg = str(arg)
            if '*' in arg:
                # get file of path in arg with Unix style pathname pattern expansion
                fileList = glob.glob(arg)
                if fileList:
                    inputFileList = fileList
                    inputPathPattern = arg
                    inputI = i
                else:
                    outputPathPattern = arg
                    outputI = i

        # maybe output directory already contained output files matching output pattern?
        assert outputPathPattern != '' and inputPathPattern != ''

        
        pre, post = inputPathPattern.split('*')
        outputFileList = []
        for fil in inputFileList:
            tmp = str(fil).replace(pre, '')
            tmp = str(tmp).replace(post, '')  
            outputFileList.append(outputPathPattern.replace('*', tmp))
        
        args_list = []
        for j in range(len(inputFileList)):
            args_new = list(args)
            args_new[inputI] = inputFileList[j]
            args_new[outputI] = outputFileList[j]
            args_new.append(operator)            
            args_list.append(args_new)
            
        if parallel:
            # multiprocessing
            num_of_workers = multiprocessing.cpu_count()
            pool = multiprocessing.Pool(num_of_workers - 1)
            # blocks until finished
            pool.map(callWrapper, args_list)
        elif parallel:
            # multiprocessing
            num_of_workers = multiprocessing.cpu_count()
            pool = multiprocessing.pool.ThreadPool(num_of_workers - 1)
            # blocks until finished
            pool.map(callWrapper, args_list)
        else:
            callWrapper(args_list[0])

        return outputPathPattern
        
def callWrapper(selfAndArgs):
    operator = selfAndArgs.pop()
    print("Asnc of operator %s , with args: %s" % (operator, selfAndArgs))
    return operator._function(*selfAndArgs)
