__author__ = 'weigl'

import msml.analytics
import msml.env

import docutils.core

msml.env.load_user_file()
msml.env.current_alphabet = msml.frontend.alphabet({'--alphabet': 'alphabet.cache',
                                                    '--exporter': 'nsofa',
                                                    '--output': None,
                                                    '--start-script': '~/.config/msmlrc.py',
                                                    '--verbose': False,
                                                    '--xsd-file': None,
                                                    '-S': True,
                                                    '-w': False,
                                                    '<file>': [],
                                                    '<paths>': [],
                                                    'alphabet': False,
                                                    'exec': True,
                                                    'show': False})

rst = msml.analytics.export_alphabet_overview_markdown()

print rst

def rst2html(rst):
    return docutils.core.publish_parts(rst, writer_name='html')['html_body']


html = rst2html(rst)

import webbrowser, tempfile, path

p = path.path(tempfile.mktemp(".html"))

with open(p, "w") as f:
    f.write(html)

webbrowser.open("file:///%s" % p.abspath())