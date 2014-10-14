__author__ = 'suwelack'

import numpy as np
from scipy import optimize
from os import path

from collections import namedtuple

class MSMLOptimizer(object):
    ReferenceType = namedtuple('ReferenceValue', 'variable_name value_name value')

    def __init__(self, simulation_runner, variables = None, reference=None, options=None):
        self._sim_runner = simulation_runner
        self._variables = variables
        self._options = options
        self._reference = reference


    def run(self):

        if self._reference is None:
            print('Error, please set reference value first')
            return None

        # initialize history
        self._history = {}

        self._history['error'] = list()

        for variable_name in self._variables:
            self._history[variable_name] = list()
            self._history[variable_name].append(list(self._variables[variable_name]))

        f_to_minimize = self._TargetFunction

        #build x0
        x0List = list()
        for variable_name in self._variables:
            x0List.extend(self._variables[variable_name])

        x0 =  np.asarray(x0List)
        #pn = optimize.fmin_cg(f_to_minimize, x0, epsilon=0.1)
        self._iter_count = 0
        if self._options is not None:
            if self._options['max_iterations']:
                result = optimize.leastsq(f_to_minimize, x0, maxfev=self._options['max_iterations'])
            else:
                result = optimize.leastsq(f_to_minimize, x0)





        return self._history

    def set_variables(self, variables):
        self._variables = variables

    def set_options(self, options):
        self._options = options

    def set_reference(self, reference):
        self._reference = reference

    def _TargetFunction(self,x0):
        self._iter_count = self._iter_count+1
        counter = 0
        for variable_name in self._variables:
            initial_value = self._variables[variable_name]
            current_value = initial_value
            if not isinstance(initial_value, list):
                print('Error, initial variable value has to be of list type')
            for i in xrange(len(initial_value)):
                current_value[i] = x0[counter]
                counter = counter+1
            #now set the variable
            self._sim_runner.update_variable(variable_name, current_value)
            self._history[variable_name].append(list(current_value))

        #if requested, save raw output
        if self._options is not None:
            rawOutputList = self._options['save_intermediate_results']

            fileName, fileExtension = path.splitext(rawOutputList['filename'])
            completeFilename = fileName + "_" + str(self._iter_count)  + fileExtension

            self._sim_runner.update_variable(rawOutputList['name'],  completeFilename)

        #run the simulation
        self._sim_runner.run()

        #for debug purpose

        #get result

        currentValue = self._sim_runner.get_results(self._reference.variable_name ,self._reference.value_name)

        currentNumpyValue =  np.asarray(currentValue)
        referenceNumpyValue =  np.asarray(self._reference.value)
        #sum of squared differences
        sum = np.sum((currentNumpyValue-referenceNumpyValue)**2)

        currentResidual = currentNumpyValue - referenceNumpyValue

        #add to history
        self._history['error'].append(sum)

        print(self._history['error'])
        for variable_name in self._variables:
            print(self._history[variable_name])


        return currentResidual







