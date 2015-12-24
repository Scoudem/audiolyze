'''
File: config.py
Author: Tristan van Vaalen

Argparser wrapper storing project config
'''

import argparse
import verbose

v = verbose.Verbose()


class Config:

    def __init__(self, setup=True):
        self.parser = None
        self.args = {}

        if setup:
            self.parser = self.create_parser()
            self.setup_arguments(self.parser)
            self.parse_arguments(self.parser)

    def create_parser(self):
        return argparse.ArgumentParser(
            description='Analyze audio streams'
        )

    def setup_arguments(self, parser):
        parser.add_argument(
            '--debug', dest='debug', action='store_true',
            help='debug mode'
        )
        parser.add_argument(
            '--silent', dest='silent', action='store_true',
            help='silent mode (no stdout)'
        )
        parser.add_argument(
            '-r', '--rate', metavar='rate', type=int,
            default=44100, help='recording rate'
        )
        parser.add_argument(
            '-l', '--length', metavar='length', type=int,
            default=2 ** 12, help='plot range'
        )
        parser.add_argument(
            '--no-response', dest='response', action='store_false',
            help='not frequency response plot'
        )
        parser.add_argument(
            '--no-z', dest='zplot', action='store_false',
            help='no zero-pole plane plot'
        )
        parser.add_argument(
            '--no-record', dest='record', action='store_false',
            help='no recording (also no stream plot)'
        )

    def parse_arguments(self, parser):

        args = parser.parse_args()

        v.set_debug(args.debug)
        v.set_silent(args.silent)

        self.args = vars(args)

        v.debug('Parsing arguments...').indent()
        for arg in self.args:
            v.write('{}: {}'.format(arg, getattr(args, arg)))

        v.unindent()
