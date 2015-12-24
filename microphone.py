'''
File: microphone.py
Author: Tristan van Vaalen

Audio stream of microphone
'''

import audiolazy
import plotable
import threading
import verbose
import signal

v = verbose.Verbose()


class Microphone:

    def __init__(self, filt, **kwargs):
        self.record = kwargs['record']
        self.rate = kwargs['rate']

        v.debug('Filter:\n{}'.format(filt))
        v.debug('is LTI: {}'.format(filt.is_lti()))
        v.debug('is causal: {}'.format(filt.is_causal()))

        if not (filt.numpoly.is_polynomial() and
                filt.denpoly.is_polynomial()):
            v.warning('Filter is not polynomial. linearizing filter...')
            filt = filt.linearize()
            v.debug('Linearized filter:\n{}'.format(filt))

        if not filt.is_causal():
            v.error('Non-causal filter given')
            raise ValueError('Non-causal filter')

        self.plotable = plotable.Plotable(filt, **kwargs)

        v.debug('Registering signal handler')
        signal.signal(signal.SIGINT, self.signal_handler)

        self.setup_recording()
        self.start()
        self.stop()

    def signal_handler(self, signal, frame):
        self.stop()

    def setup_recording(self):
        audiolazy.chunks.size = 1
        self.thread = threading.Thread(target=self._update_data)

    def _update_data(self):
        v.debug('Listening...')
        v.info('Your audio API could throw some warnings...')
        with audiolazy.AudioIO() as record:
            for element in record.record(rate=self.rate):
                self.plotable.append(element)

                if not self.running:
                    break

    def start(self):
        if self.record:
            v.debug('Starting recording thread')
            self.running = True
            self.thread.start()

        self.plotable.start_animation()

    def stop(self):
        if not self.record:
            return

        v.debug('Stopping recording thread')
        self.running = False
        self.thread.join()

if __name__ == '__main__':
    mic = Microphone()
