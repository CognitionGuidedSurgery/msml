msml
----


msml exec     [-w] [options] [<file>...]
msml show     [options] <file>
msml writexsd <XSDFile>
msml check    [<file>...]
msml validate

.. program:: msml.py

.. option:: -e EXPORTER, --exporter=VALUE

    specifies the exporter to be used: ``nsofa``, ``nabaqus``, ``hiflow3``

.. option:: -a DIR, --alphabet-dir=DIR

    specifies a search path of msml alphabet

.. option:: -m FILE, --memory=FILE

    preset the Executor memory with the given yaml file.

.. option::  -v, --verbose

   More output. Enables the Information and Debug level of :py:func:`msml.log.report`

.. option:: -o, --output=DIR

    specifies a directory for output and temporaries files

.. option:: --start-script=FILE

    rc file

