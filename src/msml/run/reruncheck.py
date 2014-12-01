# region gplv3preamble
# The Medical Simulation Markup Language (MSML) - Simplifying the biomechanical modeling workflow
#
# MSML has been developed in the framework of 'SFB TRR 125 Cognition-Guided Surgery'
#
# If you use this software in academic work, please cite the paper:
# S. Suwelack, M. Stoll, S. Schalck, N.Schoch, R. Dillmann, R. Bendl, V. Heuveline and S. Speidel,
#   The Medical Simulation Markup Language (MSML) - Simplifying the biomechanical modeling workflow,
#   Medicine Meets Virtual Reality (MMVR) 2014
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

__author__ = "Alexander Weigl <Alexander.Weigl@uiduw.student.kit>"
__date__ = "2014-11-18"
__version__ = ""

import shelve
import os
import json
import atexit
import gzip

class ReRunCheck(object):
    """This class checks if the execution of operators can be omitted.


    """

    def __init__(self, folder, gzip_mode = True):
        self.gzip = gzip_mode
        if gzip_mode:
            self._timestamp_file = folder / 'rerun.db.gz'
            self._fopen = gzip.GzipFile
        else:
            self._timestamp_file = folder / 'rerun.db'
            self._fopen = open

    def __enter__(self):
        self._timestamps = None
        try:

            with self._fopen(self._timestamp_file) as fp:
                self._timestamps = json.load(fp)
        except IOError:
            pass

        if self._timestamps is None:
            self._timestamps = dict()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        with self._fopen(self._timestamp_file, 'w') as fp:
            json.dump(self._timestamps, fp)

    def check(self, task_id, input_files, arguments, output_file):
        """Determines if you need to rerun the operator, based on modify time.

        :param input_files: the input files, also included in the arguments
         :type input_files: list[str]
        :param arguments: a dictionary of the given parameters
         :type arguments: dict[str,object]
        :param output_file: the file path of output files
         :type output_file: str

        :return:
        """

        def mtime(filename):
            try:
                return os.stat(filename).st_mtime
            except:
                return 0

        if not output_file:
            return False

        if not self.has_entry(task_id):
            r = False

        input_times = {k: mtime(k) for k in input_files}

        # no cached entry => execute task
        if not self.has_entry(task_id):
            r = False
        else:
            # rerun can omitted iff
            # 1) all input files are older than the output file
            # 2) no changes in the arguments

            output_time = mtime(output_file)
            younger = all(map(lambda a: a <= output_time, input_times.values()))

            _, old_args, _ = self.get(task_id)
            nochanges = old_args == arguments

            r = younger and nochanges

        self.store(task_id, input_times, arguments, output_file)
        return r

    def has_entry(self, task_id):
        return task_id in self._timestamps

    def store(self, task_id, input_timestamps, arguments, output_file):
        self._timestamps[task_id] = (input_timestamps, arguments, output_file)

    def get(self, task_id):
        return self._timestamps[task_id]

    def hash_results(self, task_id):
        return  task_id in  self._timestamps.get('__output__', {})

    def get_last_result(self, task_id):
        return self._timestamps.get('__output__', {})[task_id]

    def set_last_result(self, task_id, result):
        output = self._timestamps.get('__output__', {})
        output[task_id] = result
        self._timestamps["__output__"] = output