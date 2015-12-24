'''
File: plotable.py
Author: Tristan van Vaalen

Plotable data stream
'''

import collections
import numpy
import audiolazy
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import verbose

v = verbose.Verbose()


class Plotable:

    def __init__(self, filt, **kwargs):
        for key, value in kwargs.iteritems():
            setattr(self, key, value)

        self.filt = filt
        self.window = numpy.array(audiolazy.window.hamming(self.length))
        self.data = collections.deque([0.] * self.length, maxlen=self.length)
        self.seconds, self.hertz = audiolazy.sHz(self.rate)
        self.miliseconds = 1e-3 * self.seconds

        self.setup_plot()

    def append(self, element):
        self.data.append(element)

    def setup_plot(self, title='Audio stream analysis'):
        if self.record:
            self.figure = plt.figure(
                title,
                facecolor='#cccccc'
            )

            self.time_values = numpy.array(
                list(
                    audiolazy.line(
                        self.length, -self.length / self.miliseconds, 0
                    )
                )
            )
            v.debug('Buffer size: {}ms (t={} to t={})'.format(
                abs(self.time_values[0]) - self.time_values[-1],
                self.time_values[0], self.time_values[-1]
            ))

            self.freq_values = numpy.array(
                audiolazy.line(self.length, 0, 2 * audiolazy.pi / self.hertz)
                .take(self.length // 2 + 1)
            )
            v.debug('Frequency range: {}Hz to {}Hz'.format(
                self.freq_values[0], self.freq_values[-1]
            ))

            self.dft_max_min, self.dft_max_max = 0.01, 1.0
            xlim_t = (self.time_values[0], self.time_values[-1])
            ylim_t = (-1., 1.)
            xlim_f = (self.freq_values[0], self.freq_values[-1])
            ylim_f = (0., .5 * (self.dft_max_max + self.dft_max_min))

            self.time_ax, self.time_line = self._subplot_and_line(
                1, xlim_t, ylim_t, '#00aaff', 'Time (ms)'
            )

            self.time_filt_ax, self.time_filt_line = self._subplot_and_line(
                2, xlim_t, ylim_t, '#aa00ff', 'Filtered Time (ms)'
            )

            self.freq_ax, self.freq_line = self._subplot_and_line(
                3, xlim_f, ylim_f, '#00aaff', 'Frequency (Hz)'
            )

            self.freq_filt_ax, self.freq_filt_line = self._subplot_and_line(
                4, xlim_f, ylim_f, '#aa00ff', 'Filtered Frequency (Hz)'
            )

        if self.response:
            v.debug('Plotting frequency response')
            self.filt.plot()

        if self.zplot:
            v.debug('Plotting zero-pole plane')
            self.filt.zplot()

    def update_y_lim(self, ax, ax2, smax):
        top = ax.get_ylim()[1]
        if top < self.dft_max_max and abs(smax / top) > 1:
            ax.set_ylim(top=top * 2)
            ax2.set_ylim(top=top * 2)
            return True

        elif top > self.dft_max_min and abs(smax / top) < .2:
            ax.set_ylim(top=top / 2)
            ax2.set_ylim(top=top / 2)
            return True

        return False

    def _subplot_and_line(self, index, xlim, ylim, color, label):
        ax = plt.subplot(
            2, 2, index,
            xlim=xlim,
            ylim=ylim,
            axisbg='black'
        )
        ax.set_xlabel(label)

        line = ax.plot(
            [], [], linewidth=2, color=color
        )[0]

        return ax, line

    def start_animation(self):
        if self.record:
            v.debug('Starting animation')
            v.info('Large window size can seriously slow down rendering')

            self.rempty = False
            self.anim = FuncAnimation(
                self.figure,
                self.animate,
                init_func=self.init,
                interval=10,
                blit=True
            )

        # plt.ioff()
        plt.show()

    def init(self):
        self.time_line.set_data([], [])
        self.freq_line.set_data([], [])
        self.time_filt_line.set_data([], [])
        self.freq_filt_line.set_data([], [])
        self.figure.tight_layout()

        if self.rempty:
            return []
        else:
            return [
                self.time_line,
                self.freq_line,
                self.time_filt_line,
                self.freq_filt_line
            ]

    def animate(self, idx):
        if idx == 100:
            plt.savefig('test.png')

        array_data = numpy.array(self.data)
        array_data_filt = self.filt(array_data).take(audiolazy.inf)

        spectrum = numpy.abs(numpy.fft.rfft(array_data * self.window)) /\
            self.length
        spectrum_filt = numpy.abs(numpy.fft.rfft(array_data_filt * self.window)) /\
            self.length

        self.time_line.set_data(self.time_values, array_data)
        self.time_filt_line.set_data(self.time_values, array_data_filt)
        self.freq_line.set_data(self.freq_values, spectrum)
        self.freq_filt_line.set_data(self.freq_values, spectrum_filt)

        smax = spectrum.max()
        s1 = self.update_y_lim(self.freq_ax, self.freq_filt_ax, smax)

        if not s1:
            self.rempty = True
            return [
                self.time_line,
                self.freq_line,
                self.time_filt_line,
                self.freq_filt_line
            ]

        return []
