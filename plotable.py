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

    def __init__(self, filt=None, length=2 ** 12, rate=44100):
        self.filt = filt
        self.rate = rate
        self.length = length
        self.window = numpy.array(audiolazy.window.hamming(length))
        self.data = collections.deque([0.] * self.length, maxlen=self.length)
        self.seconds, self.hertz = audiolazy.sHz(self.rate)
        self.miliseconds = 1e-3 * self.seconds
        self.setup_plot()

    def append(self, element):
        self.data.append(element)

    def setup_plot(self, title='Plot'):
        v.debug('Setting up plot')
        self.figure = plt.figure(
            title,
            facecolor='#cccccc'
        )

        # Time plot
        self.time_values = numpy.array(
            list(
                audiolazy.line(self.length, -self.length / self.miliseconds, 0)
            )
        )
        self.time_ax = plt.subplot(
            3, 1, 1,
            xlim=(self.time_values[0], self.time_values[-1]),
            ylim=(-1., 1.),
            axisbg='black'
        )
        self.time_ax.set_xlabel('Time (ms)')
        self.time_plot_line = self.time_ax.plot(
            [], [], linewidth=2, color='#00aaff'
        )[0]

        # Frequency plot
        self.dft_max_min, self.dft_max_max = .01, 1.
        self.freq_values = numpy.array(
            audiolazy.line(self.length, 0, 2 * audiolazy.pi / self.hertz)
            .take(self.length // 2 + 1)
        )
        self.freq_ax = plt.subplot(
            3, 1, 2,
            xlim=(self.freq_values[0], self.freq_values[-1] / 2),
            ylim=(0., .5 * (self.dft_max_max + self.dft_max_min)),
            axisbg='black'
        )
        self.freq_ax.set_xlabel('Frequency (Hz)')
        self.freq_plot_line = self.freq_ax.plot(
            [], [], linewidth=2, color='#00aaff'
        )[0]

        # Filter plot
        self.filt_ax = plt.subplot(
            3, 1, 3,
            xlim=(self.freq_values[0], self.freq_values[-1] / 2),
            ylim=(0., .5 * (self.dft_max_max + self.dft_max_min)),
            axisbg='black'
        )
        self.filt_ax.set_xlabel('Filtered Frequency (Hz)')
        self.filt_plot_line = self.filt_ax.plot(
            [], [], linewidth=2, color='#00aaff'
        )[0]

        # Plot the response of filter
        self.filt.plot()

    def start_animation(self):
        v.debug('Starting animation')

        self.rempty = False
        self.anim = FuncAnimation(
            self.figure,
            self.animate,
            init_func=self.init,
            interval=10,
            blit=True
        )
        plt.ioff()
        plt.show()

    def init(self):
        self.time_plot_line.set_data([], [])
        self.freq_plot_line.set_data([], [])
        self.filt_plot_line.set_data([], [])
        self.figure.tight_layout()

        if self.rempty:
            return []
        else:
            return [
                self.time_plot_line, self.freq_plot_line, self.filt_plot_line
            ]

    def animate(self, idx):
        array_data = numpy.array(self.data)

        if self.filt is not None:
            array_data_filt = self.filt(array_data).take(audiolazy.inf)

        spectrum = numpy.abs(numpy.fft.rfft(array_data * self.window)) /\
            self.length

        spectrum_filt = numpy.abs(numpy.fft.rfft(array_data_filt * self.window)) /\
            self.length

        self.time_plot_line.set_data(self.time_values, array_data)
        self.freq_plot_line.set_data(self.freq_values, spectrum)
        self.filt_plot_line.set_data(self.freq_values, spectrum_filt)

        smax = spectrum.max()
        top = self.freq_ax.get_ylim()[1]
        if top < self.dft_max_max and abs(smax / top) > 1:
            self.freq_ax.set_ylim(top=top * 2)
        elif top > self.dft_max_min and abs(smax / top) < .3:
            self.freq_ax.set_ylim(top=top / 2)
        else:
            self.rempty = True
            return [
                self.time_plot_line, self.freq_plot_line, self.filt_plot_line
            ]
        return []
