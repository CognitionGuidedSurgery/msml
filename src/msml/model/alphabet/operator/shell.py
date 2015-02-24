from .base import *
from .python import *

__author__ = 'Alexander Weigl'

class ShellOperator(PythonOperator):
    """ShellOperator

    """

    def __init__(self, name, input=None, output=None, parameters=None, runtime=None, meta=None, settings=None):
        Operator.__init__(self, name, input, output, parameters, runtime, meta, settings)
        self.command_tpl = runtime['template']
        self.extract_pattern = runtime.get('ouput_pattern', None)

        self.extract_names = map(lambda s: s.strip(" ,\n"), runtime.get('output_names', '').split(' '))

    def bind_function(self):
        pass

    def _check_function(self):
        pass

    def _function(self, *args):
        kwargs =  dict(zip(self.acceptable_names(), args))
        command = self.command_tpl.format(**kwargs).strip()
        executable = str(msml.env.binary_search_path)
        log.debug("Execute: %s", command)
        proc = subprocess.Popen(command,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT,
                                shell=True,
                                env={'PATH' : executable})
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
            log.error("%s return with nonzero", args)
            raise BaseException("%s return with nonzero" % args)

