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

    def __init__(self, filt=None, rate=44100):
        self.filt = filt

        self.rate = rate
        self.plotable = plotable.Plotable(filt=filt, rate=rate)

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
        with audiolazy.AudioIO() as record:
            for element in record.record(rate=self.rate):
                self.plotable.append(element)

                if not self.running:
                    break

    def start(self):
        v.debug('Starting recording thread')
        v.warning('PyAudio could throw some warnings...')
        self.running = True
        self.thread.start()
        self.plotable.start_animation()

    def stop(self):
        v.debug('Stopping recording thread')
        self.running = False
        self.thread.join()

if __name__ == '__main__':
    mic = Microphone()
