'''
File: waveaudio.py
Author: Tristan van Vaalen

Load a wav file
'''

import verbose
import wave
import numpy

v = verbose.Verbose()


class WaveAudio:

    def __init__(self, filename):
        fp = self._open(filename)

        self.filename = filename
        self.nchannels, self.samplewidth,\
            self.framerate, self.nframes,\
            self.comptype, self.compname = self._analyze(fp)

        frames = self._read_all(fp, self.nframes)

        self._close()

        self.samples = self._process_frames(
            frames, self.samplewidth. self.channels
        )

    def _read_n_frames(self, fp, n):
        return fp.readframes(n)

    def _process_frames(self, frames, samplewidth, channels):
        if samplewidth == 1:
            dtype = numpy.uint8
            maxvalue = 2 ** 8
        elif samplewidth == 2:
            dtype = numpy.int16
            maxvalue = 2 ** (16 - 1)
        elif samplewidth == 4:
            dtype = numpy.int32
            maxvalue = 2 ** (32 - 1)
        else:
            v.error('Unsupported samplewidth {}'.format(samplewidth))
            raise ValueError()

        all_samples = numpy.fromstring(frames, dtype)

        combined_samples = numpy.zeros(len(frames))

        for i in xrange(channels):
            a = combined_samples
            b = all_samples[i::channels]
            condition = numpy.less(numpy.abs(a), numpy.abs(b))
            combined_samples = numpy.choose(condition, [a, b])

        normalized_samples = combined_samples / maxvalue
        if dtype == numpy.uint8:
            normalized_samples = 2 * normalized_samples - 1

        return normalized_samples

    def _analyze(self, fp):
        return fp.getparams()

    def _open(self, filename):
        v.debug('Opening \'{}\''.format(filename))
        return wave.open(filename, "r")

    def _close(self, fp):
        v.debug('Closing \'{}\''.format(self.filename))
        return wave.close(fp)
