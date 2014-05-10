__author__ = 'weigl'

import msml.analytics
import msml.env
from msml.frontend import App

import docutils.core

app = App()

if True:
    rst = msml.analytics.export_alphabet_overview_rst()

    print rst

    def rst2html(rst):
        return docutils.core.publish_parts(rst, writer_name='html')['html_body']


    html = rst2html(rst)

    import webbrowser, tempfile, path

    p = path.path(tempfile.mktemp(".html"))

    with open(p, "w") as f:
        f.write(html)

    with open("alphabet.rst", "w") as f:
        f.write(rst)

    webbrowser.open("file:///%s" % p.abspath())

if 0:
    from pprint import pprint
    print "\n".join(map(str, msml.analytics.check_element_completeness()))