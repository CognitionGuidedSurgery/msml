# encoding: utf-8
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


"""This module provide basic logging facilities in color.
"""
import contextlib

__author__ = "Alexander Weigl"
__date__ = "2014-05-05"

import inspect
import os.path

import logging
import logging.config

try:
    import colorama
except:
    pass
else:
    colorama.init()

__all__ = ['_reported', 'ColoredFormatter', 'logger']

_reported = []


# # below from https://github.com/borntyping/python-colorlog/blob/master/colorlog/colorlog.py
default_log_colors = {
    'DEBUG': 'white',
    'INFO': 'green',
    'WARNING': 'yellow',
    'ERROR': 'red',
    'CRITICAL': 'bold_red',
}

# Returns escape codes from format codes
esc = lambda *x: '\033[' + ';'.join(x) + 'm'

# The initial list of escape codes
escape_codes = {
    'reset': esc('0'),
    'bold': esc('01'),
}

# The color names
COLORS = [
    'black',
    'red',
    'green',
    'yellow',
    'blue',
    'purple',
    'cyan',
    'white'
]

PREFIXES = [
    # Foreground without prefix
    ('3', ''), ('01;3', 'bold_'),

    # Foreground with fg_ prefix
    ('3', 'fg_'), ('01;3', 'fg_bold_'),

    # Background with bg_ prefix - bold/light works differently
    ('4', 'bg_'), ('10', 'bg_bold_'),
]

for prefix, prefix_name in PREFIXES:
    for code, name in enumerate(COLORS):
        escape_codes[prefix_name + name] = esc(prefix + str(code))

import sys


class ColoredFormatter(logging.Formatter):
    """A formatter that allows colors to be placed in the format string.

    Intended to help in creating more readable logging output."""

    def __init__(self, format, datefmt=None,
                 log_colors=default_log_colors, reset=True, style='%'):
        """
        :Parameters:
        - format (str): The format string to use
        - datefmt (str): A format string for the date
        - log_colors (dict):
            A mapping of log level names to color names
        - reset (bool):
            Implictly append a color reset to all records unless False
        - style ('%' or '{' or '$'):
            The format style to use. No meaning prior to Python 3.2.

        The ``format``, ``datefmt`` and ``style`` args are passed on to the
        Formatter constructor.
        """
        if sys.version_info > (3, 2):
            super(ColoredFormatter, self).__init__(
                format, datefmt, style=style)
        elif sys.version_info > (2, 7):
            super(ColoredFormatter, self).__init__(format, datefmt)
        else:
            logging.Formatter.__init__(self, format, datefmt)
        self.log_colors = log_colors
        self.reset = reset

    def format(self, record):
        # Add the color codes to the record
        record.__dict__.update(escape_codes)

        # If we recognise the level name,
        # add the levels color as `log_color`
        if record.levelname in self.log_colors:
            color = self.log_colors[record.levelname]
            record.log_color = escape_codes[color]
        else:
            record.log_color = ""

        # Format the message
        if sys.version_info > (2, 7):
            message = super(ColoredFormatter, self).format(record)
        else:
            message = logging.Formatter.format(self, record)

        # Add a reset code to the end of the message
        # (if it wasn't explicitly added in format str)
        if self.reset and not message.endswith(escape_codes['reset']):
            message += escape_codes['reset']

        return message

def set_verbosity(log_level):
    LEVELS = { x : getattr(logging, x)
               for x in ('CRITICAL', 'FATAL', 'ERROR', 'WARNING', 'WARN', 'INFO', 'DEBUG', 'NOTSET')}

    if log_level in LEVELS:
        log_level = LEVELS[log_level]

    for handler in logging._handlers.values():
        handler.level = log_level


## https://docs.python.org/2/library/logging.html#logrecord-attributes
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'long':{
          'format': "%(asctime)-20s %(levelname)-8s %(name)-20s  %(message)s [%(filename)s:%(lineno)d in %(module)s:%(funcName)s]"
        },
        'default': {
            'format': '%(asctime)s %(levelname)s %(name)s %(message)s'
        },
        'color': {
            '()': ColoredFormatter,
            'format': "%(log_color)s%(levelname)-8s%(reset)s %(blue)s%(message)s"
        }
    },
    'handlers': {
        'file': {
            '()': 'logging.FileHandler',
            'level': 'DEBUG',
            'formatter': 'long',
            'filename': 'msml.log',
            'mode': 'w',
            'encoding': 'utf-8',
        },
        'console': {
            '()': 'logging.StreamHandler',
            'stream': sys.stdout,
            'level': 'INFO',
            'formatter': 'color',
        },
    },
    'root': {
        'handlers': ['file', 'console'],
        'level': 'DEBUG',
    },
}
logging.config.dictConfig(LOGGING)
logger = logging.getLogger("root")




from multiprocessing import Lock
from functools import wraps

logger_lock = Lock()
def thread_safe(func):
    @wraps(func)
    def acrel(*args, **kwargs):
        logger_lock.acquire()
        r = func(*args, **kwargs)
        logger_lock.release()
        return r
    return acrel

error     = thread_safe(logger.error)
warn      = thread_safe(logger.warn)
info      = thread_safe(logger.info)
debug     = thread_safe(logger.debug)
critical  = thread_safe(logger.critical)
exception = thread_safe(logger.exception)
fatal     = thread_safe(logger.fatal)

import  decorator

@contextlib.contextmanager
def timeit(message):
    import time
    starttime = time.time()
    yield starttime
    endtime = time.time()
    info("%s took %f s"  % (message, endtime-starttime))