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

    def __init__(self, rate=44100):
        self.rate = rate
        self.plotable = plotable.Plotable(rate=rate)

        v.debug('Registering signal handler')
        signal.signal(signal.SIGINT, self.signal_handler)

        self.setup_recording()
        self.start()
        self.stop()

    def signal_handler(self, signal, frame):
        self.stop()

    def setup_recording(self):
        audiolazy.chunks.size = 16
        self.thread = threading.Thread(target=self._update_data)

    def _update_data(self):
        with audiolazy.AudioIO() as record:
            for element in record.record(rate=self.rate):

                # v.rewrite(element)
                self.plotable.append(element)

                if not self.running:
                    break

    def start(self):
        v.debug('Starting recording thread')
        v.info('PyAudio could throw some warnings now (not guaranteed)...')
        self.running = True
        self.thread.start()
        self.plotable.start_animation()

    def stop(self):
        v.write('')
        v.debug('Stopping recording thread')
        self.running = False
        self.thread.join()

if __name__ == '__main__':
    mic = Microphone()
