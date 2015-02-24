from .python import *

__author__ = 'Alexander Weigl'

class SharedObjectOperator(PythonOperator):
    """Shared Object Call via ctype"""
    # TODO: executeOperatorSequence

    def __init__(self, name, input=None, output=None, parameters=None, runtime=None, meta=None):
        super(Operator, self).__init__(name, input, output, parameters, runtime, meta)
        self.symbol_name = runtime['symbol']
        self.filename = runtime['file']

    def bind_function(self):
        import ctypes

        object = ctypes.CDLL(self.filename)

        self.__function = getattr(object, self.symbol_name)
        return self.__function

