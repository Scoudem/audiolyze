'''
File: Audiolyze.py
Author: Tristan van Vaalen

Audio stream analyzer
'''

import config
import microphone
from audiolazy import z
# import audiolazy


class Audiolyze:

    def __init__(self, filt):
        self.config = config.Config()
        self.microphone = microphone.Microphone(filt, **self.config.args)

if __name__ == '__main__':
    # filt = (0.2 * (1 - z ** 5)) / (z ** 4)(1 - z)
    # filt = 0.2 * (1 + z ** -1 + z ** -2 + z ** -3 + z ** -4)
    # filt = 0.2 * (1 - z**5) / (z**2 * (1-z))
    # filt = 0.03824 * (z**2 - 1) / (z**2 + 0.9235)
    # filt = (-z + 3)/(z - 9.5)
    # filt = (0.18 * z) / ((z - 1) * (z - 0.82))
    # filt = audiolazy.comb.tau(delay=30*2, tau=40*4)
    filt = 1 / ((2 * (z - 1)) / (0.1 * (z + 1)) + 1)
    # filt = 1 - z ** -1
    audiolyze = Audiolyze(filt)
