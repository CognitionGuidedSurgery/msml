from .base import *

__author__ = 'Alexander Weigl'

from .... import log
from ....log import error
from ...sequence import executeOperatorSequence

class PythonOperator(Operator):
    """Operator for Python functions.

    """

    def __init__(self, name, input=None, output=None, parameters=None, runtime=None, meta=None, settings=None):
        """
        :param runtime: should include the key: "function" and "module"
        .. seealso: :py:meth:`Operator.__init__`
        """
        Operator.__init__(self, name, input, output, parameters, runtime, meta, settings)
        self.function_name = runtime['function']
        """name of the pyhton function"""
        self.modul_name = runtime['module']
        """the name of the python module"""
        self._function = None
        """the found and bind python function"""

    def _check_function(self):
        pass

    def __str__(self):
        return "<PythonOperator: %s.%s>" % (self.modul_name, self.function_name)

    def __call__(self, **kwargs):
        if not self._function:
            self.bind_function()

        # bad for c++ modules, because of loss of signature
        # r = self.__function(**kwargs)

        #replace empty values with defaults from operators xml description (by getting all defaults and overwrite with given user values)
        kwargsUpdated = self.get_default_args()
        kwargsUpdated.update(kwargs)

        args = [kwargsUpdated.get(x, None) for x in self.acceptable_names()]
        orderedKwArgs = OrderedDict(zip(self.acceptable_names(), args))

        log.debug("Parameter: %s" % self.acceptable_names() )
        log.debug("Args: %s" % args)

        count = sum('*' in str(arg) for arg in kwargsUpdated.values())
        if count == 2:
            r = executeOperatorSequence(self, orderedKwArgs, self.settings.get('seq_parallel', True))
        else:
            r = self._function(*args)

        if len(self.output) == 0:
            results = None
        elif len(self.output) == 1:
            results = {self.output_names()[0]: r}
        else:
            results = dict(zip(self.output_names(), r))

        return results

    def bind_function(self):
        """Search and bind the python function. Have to be called before `__call__`"""
        import importlib

        try:
            mod = importlib.import_module(self.modul_name)
            self._function = getattr(mod, self.function_name)

            return self._function
        except ImportError as e:
            #TODO print stack traces
            error("%s.%s is not available (module not found), got exception message '%s'" % (self.modul_name, self.function_name, e.message))
        except AttributeError as e:
            error("%s.%s is not available (function/attribute not found), got exception message '%s" % (self.modul_name, self.function_name, e.message))


    def validate(self):
        return self.bind_function() is not None
