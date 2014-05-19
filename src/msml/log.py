# encoding: utf-8

"""This module provide basic logging facilities in color.
"""

__author__ = "Alexander Weigl"
__date__ = "2014-05-05"

import inspect
import os.path

__all__ = ['report']

COLOR_TABLE = {'I': 94, 'W': 33, 'E': 31, 'D': 90, 'F': 35}

FORMAT = "{color}{type}-{number}: {msg} {grey}(from {file}:{lineno}){nocolor}"


def report(msg, kind="W", number=0, filename=None, lineno=-1):
    """prints a report information on stdout

    if `filename` is empty, the method tries to find the source of the caller.

    :param msg: Message
    :type msg: str
    :param kind: I, W, E, D, F -- kind of message
    :param number: some random error number
    :param filename: a filename (location of event)
    :param lineno: a line number (location of event)
    :return:
    """
    if not filename:
        frame = inspect.stack()[1][0]
        info = inspect.getframeinfo(frame)

        color = COLOR_TABLE.get(kind, 0)

        filename = os.path.basename(info.filename)
        lineno = info.lineno
        if filename == "__init__.py":
            filename = os.path.join(os.path.basename(
                os.path.dirname(info.filename)), filename)

    print FORMAT.format(
        type=kind,
        number=number,
        lineno=lineno,
        file=filename,
        msg=msg,
        color="\x1b[%dm" % color,
        nocolor="\x1b[0m",
        grey="\x1b[37m"
    )
