import jinja2
from .base import *
from .python import *
import os, subprocess, re
from ....env import binary_search_path



__author__ = 'Alexander Weigl'

__all__ = ['ShellOperator']

jinja_env = jinja2.Environment(auto_reload=False)

def flag(value, name):
    if value:
        return "-%s" % name
    else:
        return ""


def option(value, name):
    if value is not None:
        return "-%s %s" % (name, value)
    return ""

jinja_env.filters['flag'] = flag
jinja_env.filters['option'] = option


class ShellOperator(PythonOperator):
    """ShellOperator

    """

    def __init__(self, name, input=None, output=None, parameters=None, runtime=None, meta=None, settings=None):
        Operator.__init__(self, name, input, output, parameters, runtime, meta, settings)
        self.command_tpl = runtime['template']
        self.extract_pattern = runtime.get('output_pattern', None)
        self.extract_names = map(lambda s: s.strip(" ,\n"), runtime.get('output_names', '').split(' '))

        self._template = jinja_env.from_string(self.command_tpl)


    def bind_function(self):
        pass

    def _check_function(self):
        pass

    def command(self, kwargs):
        return self._template.render(**kwargs)

    def _function(self, *args):
        kwargs =  dict(zip(self.acceptable_names(), args))
        command = self.command(kwargs).strip()
        env_path = str(binary_search_path)
        ld_library_path = os.environ.get("LD_LIBRARY_PATH", '') + ":" + env_path
        log.debug("Execute: %s", command)
        proc = subprocess.Popen(command,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT,
                                shell=True,
                                env={'PATH' : env_path,
                                     'LD_LIBRARY_PATH' : ld_library_path})
        proc.wait()
        output = proc.stdout.read()

        for line in output.splitlines():
            log.debug("%s: %s", command, line)

        if proc.returncode == 0:
            if self.extract_pattern:
                rp = re.compile(self.extract_pattern, re.MULTILINE | re.DOTALL)
                matcher = rp.match(output)
                if matcher:
                    try:
                        # no error case
                        return [matcher.group(n) for n in self.extract_names]
                    except KeyError as e:
                        log.error("output of %s is not within the regex %s",e.message, self.extract_pattern )
                        raise
                else:
                    log.error("regex %r not matched previous output", self.extract_pattern)
                    raise BaseException("regex %r not matched previous output" % self.extract_pattern)
            else:
                return list()
        else:
            log.error("%s return with nonzero (%d)", command, proc.returncode)

            if proc.returncode == 127: # command not found
                log.error("Return code is 127, command not found (linux).\nThe search path was: %s", env_path.replace(":", "\n"))


            raise BaseException("%s return with nonzero" % command)