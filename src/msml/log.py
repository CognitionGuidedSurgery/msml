# !/usr/bin/env python
# encoding: utf-8

"""
https://stackoverflow.com/questions/384076/how-can-i-color-python-logging-output
"""

from __future__ import print_function
import ansi

t = ansi.term()
print = t.printr
t.register("error",
           ansi.style(foreground=ansi.Color16Table.White,
                      background=ansi.Color16Table.Red))

t.register("ptype_error",
           ansi.style(foreground=ansi.Color16Table.White,
                      background=ansi.Color16Table.Red,
                      option=ansi.Option.BOLD_ON))

t.register("slot_sort_error",
           ansi.style(foreground=ansi.Color16Table.White,
                      background=ansi.Color16Table.Red,
                      option=ansi.Option.BOLD_ON))

t.register("ltype_error",
           ansi.style(foreground=ansi.Color16Table.White,
                      background=ansi.Color16Table.Red))

def p(s): t.cprint(s+"\n")