# Copyright (c) 2012 Giorgos Verigakis <verigak@gmail.com>
# Modified: Alexander Weigl
#
# Permission to use, copy, modify, and distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
from __future__ import print_function

from functools import partial
import re

__version__ = '1.0.3'

COLORS = ('black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan',
          'white',
          'brightblack', 'brightred', 'brightgreen', 'brightyellow',
          'brightblue', 'brightmagenta', 'brightcyan', 'brightwhite')
STYLES = ('none', 'bold', 'faint', 'italic', 'underline', 'blink',
          'blink2', 'negative', 'concealed', 'crossed')


def color(s, fg=None, bg=None, style=None):
    return ''.join( colortpl(s, fg, bg, style) )

def colortpl(s, fg=None, bg=None, style=None):
    sgr = []

    if fg:
        if fg in COLORS:
            fgindex = COLORS.index(fg)
            if fgindex < 8:
                sgr.append(str(30 + fgindex))
            else:
                sgr.append('38;5;%d' % fgindex)
        elif isinstance(fg, int) and 0 <= fg <= 255:
            sgr.append('38;5;%d' % int(fg))
        else:
            raise Exception('Invalid color "%s"' % fg)

    if bg:
        if bg in COLORS:
            bgindex = COLORS.index(bg)
            if bgindex < 8:
                sgr.append(str(40 + bgindex))
            else:
                sgr.append('48;5;%d' % bgindex)
        elif isinstance(bg, int) and 0 <= bg <= 255:
            sgr.append('48;5;%d' % bg)
        else:
            raise Exception('Invalid color "%s"' % bg)

    if style:
        for st in style.split('+'):
            if st in STYLES:
                sgr.append(str(STYLES.index(st)))
            else:
                raise Exception('Invalid style "%s"' % st)

    if sgr:
        prefix = '\x1b[' + ';'.join(sgr) + 'm'
        suffix = '\x1b[0m'
        return prefix, s, suffix
    else:
        return "", s, ""


def strip_color(s):
    return re.sub('\x1b\[.+?m', '', s)



TAGS = {}
def register_tag(name, **kwargs ):
    TAGS[name] = kwargs

def cprintln(string, startenv="{", endenv="}"):
    cprint(string + "\n", startenv, endenv )

def cprint(string, startenv="{", endenv="}"):
    stack = []

    def pop():
        try:
            stack.pop()
            print('\x1b[0m', end="")  # restore normal
            peak()
        except:
            pass

    def push():
        tag = ""
        for tag in itokens:
            if "" != tag.strip():
                break
        next(itokens)  # consume next empty step
        stack.append(tag)
        peak()

    def peak():
        try:
            t = stack[-1]
            print(tag2color(t)[0], end= "")
        except:
            pass

    tokens = re.split(r'(\w+|[}{])', string)
    itokens = iter(tokens)
    for t in itokens:
        if t == '': continue
        elif t == startenv: push()
        elif t == endenv: pop()
        else: print(t, end="")
    else:
        pass #print(string)

def tag2color(tag):
    try:
        return colortpl('', **TAGS[tag])
    except KeyError:
        print ("Could not find %s tag" % tag)

for c in COLORS:
    register_tag("f%s" % c, fg=c)
    register_tag("b%s" % c, bg=c)

for s in STYLES:
    register_tag("s%s" % s, style=s)

# Foreground shortcuts
black = partial(color, fg='black')
red = partial(color, fg='red')
green = partial(color, fg='green')
yellow = partial(color, fg='yellow')
blue = partial(color, fg='blue')
magenta = partial(color, fg='magenta')
cyan = partial(color, fg='cyan')
white = partial(color, fg='white')
brightblack = partial(color, fg='black')
brightred = partial(color, fg='red')
brightgreen = partial(color, fg='green')
brightyellow = partial(color, fg='yellow')
brightblue = partial(color, fg='blue')
brightmagenta = partial(color, fg='magenta')
brightcyan = partial(color, fg='cyan')
brightwhite = partial(color, fg='white')

# Style shortcuts
bold = partial(color, style='bold')
none = partial(color, style='none')
faint = partial(color, style='faint')
italic = partial(color, style='italic')
underline = partial(color, style='underline')
blink = partial(color, style='blink')
blink2 = partial(color, style='blink2')
negative = partial(color, style='negative')
concealed = partial(color, style='concealed')
crossed = partial(color, style='crossed')
