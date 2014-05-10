__author__ = 'weigl'
__version__ = '0.1alpha'

from argparse import ArgumentParser
from itertools import chain

from msml.frontend import *
from msml.model.alphabet import *


msml = App(novalidate=True)


def build_argparse():
    parser = ArgumentParser(prog="run-msml-operator.py", description="""
        Let you execute every msml operator in the alphabet.
    """, version=__version__)

    subparsers = parser.add_subparsers(dest='operator_name')

    for op in msml.alphabet.operators.values():
        assert isinstance(op, Operator)

        op_args = subparsers.add_parser(op.name,
                                        help=op.meta.get('doc'))

        for i in chain(op.input.values(), op.parameters.values()):
            isinstance(i, Slot)
            op_args.add_argument("--%s" % i.name,
                                 help="wait for merge",
                                 default=i.default)

    return parser


def run_operator(name, kwargs):
    operator = msml.alphabet.get(name)
    operator.validate()
    print operator(**kwargs)


def main():
    parser = build_argparse()
    ns = parser.parse_args()

    dct = vars(ns)
    print ns
    name = dct.get('operator_name')
    del dct['operator_name']
    run_operator(name, dct)


main()