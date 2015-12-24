'''
File: Audiolyze.py
Author: Tristan van Vaalen

Audio stream analyzer
'''

import config
import microphone
from audiolazy import z, x


class Audiolyze:

    def __init__(self, filt):
        self.config = config.Config()
        self.microphone = microphone.Microphone(filt, **self.config.args)

if __name__ == '__main__':
    filt = 1 - (0.2 * z ** -4.3)
    audiolyze = Audiolyze(filt)
