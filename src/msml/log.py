# !/usr/bin/env python
# encoding: utf-8

"""
https://stackoverflow.com/questions/384076/how-can-i-color-python-logging-output
"""

import inspect
import os.path
import enum


color_table = {'I': 94, 'W': 33, 'E': 31, 'D': 90, 'F': 35}



def report(msg, type="W", number=0, filename = None, lineno = -1):
    if not filename:
        frame = inspect.stack()[1][0]
        info = inspect.getframeinfo(frame)

        c = color_table.get(type, 0)

        filename = os.path.basename(info.filename)
        if filename == "__init__.py":
            filename = os.path.join(os.path.basename(os.path.dirname(info.filename)), filename)

    print "{color}{type}-{number}: {msg} {grey}(from {file}:{lineno}){nocolor}".format(
        type=type,
        number=number,
        lineno=info.lineno,
        file=filename,
        msg=msg,
        color="\x1b[%dm" % c,
        nocolor="\x1b[0m",
        grey="\x1b[37m"
    )