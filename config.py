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
        v.debug('Initializing config').indent()

        self.parser = None

        if setup:
            self.parser = self.create_parser()
            self.setup_arguments(self.parser)
            self.parse_arguments(self.parser)

        v.unindent()

    def create_parser(self):
        v.debug('Creating argparser')

        return argparse.ArgumentParser(
            description='Analyze audio streams'
        )

    def setup_arguments(self, parser):
        v.debug('Adding argparse arguments')

        # parser.add_argument(
        #     '-f', metavar='filter', type=str, required=True,
        #     help=''
        # )
        # parser.add_argument(
        #     '--train', metavar='training files', type=str,
        #     help='Files to analyze and store in database as training.'
        # )
        # parser.add_argument(
        #     '-f', metavar='file', type=str,
        #     help='File to classify.'
        # )
        pass

    def parse_arguments(self, parser):
        v.debug('Parsing arguments')

        return parser.parse_args()
