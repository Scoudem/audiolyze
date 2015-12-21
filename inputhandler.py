'''
File: input.py
Author: Tristan van Vaalen

Handles user input
'''

import signal
import sys
import verbose

v = verbose.Verbose()


class InputHandler():

    def __init__(self):
        v.debug('Initializing input handler').indent()
        self.running = True
        self.signal_level = 0

        v.debug('Registering signal handler').unindent()
        signal.signal(signal.SIGINT, self.signal_handler)

    def test(self):
        pass

    def signal_handler(self, signal, frame):
        self.signal_level += 1

        if self.signal_level == 1:
            self.running = False
        else:
            sys.exit(0)

    def output_options(self):
        v.write(
            'Available options:\n' +
            ' - help: prints this message\n' +
            ' - exit: exit program'
            ' - test: magic'
        )

    def get(self):
        v.debug('Entering input loop')

        v.write('AUDIOLYZE v0.01\nPress ctrl+D to exit')
        while self.running:
            try:
                self._parse_input(raw_input('>>> '))
            except EOFError:
                v.write('EOF received')
                self.running = False

        v.write('Goodbye')

    def _parse_input(self, raw):
        raw = raw.strip()

        if raw in ['help', 'h', '?']:
            self.output_options()

        elif raw in ['quit', 'exit', 'stop', 'abort']:
            self.running = False

        elif raw in ['test']:
            self.test()

        else:
            v.write(
                'Invalid command \'{}\'. Try \'help\' for a list of commands'
                .format(raw)
            )
