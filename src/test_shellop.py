__author__ = 'weigl'

import msml.log

msml.log.set_verbosity('DEBUG')

import msml.frontend as F
a = F.App()
a.alphabet.operators['date']
opdate = a.alphabet.operators['date']
print opdate()

