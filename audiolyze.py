'''
File: Audiolyze.py
Author: Tristan van Vaalen

Audio stream analyzer
'''

import config
import microphone
import audiolazy


class Audiolyze:

    def __init__(self, filt):
        self.config = config.Config()
        self.microphone = microphone.Microphone(filt=filt)

if __name__ == '__main__':
    filt = 1 - audiolazy.z ** -1
    audiolyze = Audiolyze(filt)
