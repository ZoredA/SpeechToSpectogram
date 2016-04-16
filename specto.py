# This file actually uses numpy to make spectograms!
# As input, this file expects sampled audio (in the time domain) like what you would find in a wav file. Actually
# that is exactly what we expect and maybe only what we expect.

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import math

#Reference: http://stackoverflow.com/a/1303325
#Reference: http://matplotlib.org/examples/pylab_examples/specgram_demo.html
#Reference: http://stackoverflow.com/a/18625294
#Reference: http://stackoverflow.com/questions/35932145/plotting-with-matplotlib-specgram

#frequency limit: http://stackoverflow.com/a/19470773

#samplingFreq is of the form ___/sec (e.g. 44000 bits/sec)
#the inverse of samplingFreq will be used on the x-axis.

NUMBER_OF_GRID_PLOTS = 9

class Specto():
    text = None
    text_ax = None
    #plt = None
    plt.ion()

    def __init__(self):
        #plt.close("all")
        pass

    def add_text(self, new_text):
        plt.figure("Specto Figure")
        if self.text_ax is None:
            ax2 = plt.subplot2grid((3, 2), (2, 0), colspan=2)
            ax2.get_xaxis().set_visible(False)
            ax2.get_yaxis().set_visible(False)
            self.text = ax2.text(0.05, 0.95, new_text, horizontalalignment='left',
                verticalalignment='top',
                transform=ax2.transAxes)
            self.text_ax = ax2
        else:
            self.text.remove()
            self.text = self.text_ax.text(0.05, 0.95, new_text, horizontalalignment='left',
                verticalalignment='top',
                transform=self.text_ax.transAxes)

        plt.draw()

    def create_specto(self, data, args):

        # Time signal generation taken from http://stackoverflow.com/a/18625294
        frame_rate = args['Fs']
        t = np.linspace(0, len(data)/frame_rate, num=len(data))

        x = plt.figure("Specto Figure", figsize=(10, 10))

        ax0 = plt.subplot2grid((3, 2), (0, 0), colspan=2)
        ax0.plot(t, data)
        ax0.set_title('Time Domain')
        ax0.set_xlabel('Time (seconds)')
        ax0.set_ylabel('Amplitude')
        # number of rows, number of columns, plot number
        # http://matplotlib.org/api/pyplot_api.html#matplotlib.pyplot.subplot
        #ax1 = plt.subplot(2,1,2)
        ax1 = plt.subplot2grid((3,2), (1,0), colspan=2)
        Pxx, freqs, bins, im = band_limited_specgram(data, **args)
        ax1.set_title("Spectogram.")
        ax1.set_xlabel('Time (seconds)')
        ax1.set_ylabel('Frequency (hz)')

        # print(get_avg_energy(Pxx))
        #print(get_average_amp_in_chunk(bins, data))
        #plt.show()
        plt.subplots_adjust(left=0.11, bottom=0.07, right=0.9, top=0.95, wspace=0.20, hspace=0.69)
        return plt

    def create_freq_grid(self, signal, fs):
        max_time = len(signal)/fs
        fig = plt.figure("freq_grid", figsize=(12, 12))
        # We take our original time signal and split it into chunks
        time_increments = max_time/NUMBER_OF_GRID_PLOTS

        # size_of_each_plot = math.ceil(len(signal)/NUMBER_OF_GRID_PLOTS)
        chunked = np.array_split(signal, NUMBER_OF_GRID_PLOTS)
        cur_row = 0
        cur_column = 0
        current_time = 0.0
        for index, data in enumerate(chunked):
            freq, y = self.get_freq_amp(data, fs)
            ax1 = plt.subplot2grid((3, 3), (cur_row, cur_column))
            ax1.plot(freq, y, 'r')  # plotting the spectrum
            if index < NUMBER_OF_GRID_PLOTS-1:
                ax1.set_title('%4.2f to %4.2f s' % (current_time, current_time+time_increments))
            else:
                ax1.set_title('%4.2f to %4.2f s' % (current_time, max_time))
            current_time += time_increments
            ax1.set_xlabel('Freq (Hz)')
            ax1.set_ylabel('dB (10 Log)')
            cur_column += 1
            if cur_column > 2:
                cur_column = 0
                cur_row += 1
        plt.subplots_adjust(left=0.12, bottom=0.10, right=0.9, top=0.94, wspace=0.22, hspace=0.31)
        plt.show()

    # Some inspiration from http://glowingpython.blogspot.ca/2011/08/how-to-plot-frequency-spectrum-with.html
    # and http://stackoverflow.com/questions/15382076/plotting-power-spectrum-in-python
    def get_freq_amp(self, signal, fs):
        """Returns the fourier transform of the signal along with the frequencies
            Returns tuple :(freq, 10log fft)
                -freq: list of frequencies (x-axis)
                -10 log fft (y-axis)
        """
        #Y = np.abs(np.fft.fft(signal)) ** 2
        Y = np.multiply(10, np.log10(np.fft.fft(signal)))
        n = len(signal)
        freq = np.fft.fftfreq(n, d=1/fs)

        cut_list = []
        idx = np.argsort(freq)

        zero = np.float64(0)
        max_freq = np.float64(4000.0)
        for index in idx:
            if 0 <= freq[index] <= max_freq:
                cut_list.append(index)

        return freq[cut_list], Y[cut_list]

    def create_time_grid(self, signal, fs):
        max_time = len(signal) / fs
        total_time = np.linspace(0, len(signal) / fs, num=len(signal))
        fig = plt.figure("time_grid", figsize=(12, 12))
        size_of_each_plot = math.ceil((len(signal) / fs) / NUMBER_OF_GRID_PLOTS)
        #chunked = chunks(signal, size_of_each_plot)
        chunked = np.array_split(signal, NUMBER_OF_GRID_PLOTS)
        chunked_t = np.array_split(total_time, NUMBER_OF_GRID_PLOTS)

        time_increments = max_time / NUMBER_OF_GRID_PLOTS
        cur_row = 0
        cur_column = 0
        current_time = 0.0

        for index, data in enumerate(chunked):
            t = chunked_t[index]
            ax1 = plt.subplot2grid((3, 3), (cur_row, cur_column))
            ax1.plot(t, data, 'r')  # plotting the spectrum
            if index < NUMBER_OF_GRID_PLOTS - 1:
                ax1.set_title('%4.2f to %4.2f s' % (current_time, current_time + time_increments))
            else:
                ax1.set_title('%4.2f to %4.2f s' % (current_time, max_time))
            current_time += time_increments
            ax1.set_xlabel('Time (s)')
            ax1.set_ylabel('Amplitude')
            cur_column += 1
            if cur_column > 2:
                cur_column = 0
                cur_row += 1

        plt.subplots_adjust(left=0.12, bottom=0.10, right=0.9, top=0.94, wspace=0.22, hspace=0.31)
        plt.show()

    def get_time_amp(self, signal, fs):
        """This returns a tuple with (t, amp)"""

        return ()

# plt is a plot object. title is title.
# scores are the y values, e.g. [95]
# groups can be given, and if they are not, the x-axis won't have
# labels.
def create_bar_chart(plt, title, scores, y_label='',groups=None):
    # Reference: http://matplotlib.org/examples/api/barchart_demo.html

    ind = np.arange(len(scores))
    width = 0.35

    #ax = plt.subplot(2, 1, 1)
    ax = plt.subplot2grid((2,2), (0, 0))
    rects = ax.bar(ind, scores, width, color='r')
    ax.set_ylabel(y_label)
    ax.set_title(title)
    ax.set_xticks(ind + width)
    ax.set_autoscalex_on(True)
    ax.set_xlim([0, 1])

    if groups is not None:
        ax.set_xticklabels(groups)

    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width() / 2., 1.05 * height,
                '%d' % int(height),
                ha='center', va='bottom')

    plt.show()


# Goes over a signal and bins and calculates
# the average for each section.
def get_average_amp_in_chunk(bins, signal):
    chunked = list(chunks(signal, len(bins)))
    ret_list = []
    for index, i in enumerate(chunked):
        ret_list.append((bins[index],  np.average(i)))

    return ret_list

# Taken from http://stackoverflow.com/a/312464
def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

# Looks at a len(times) x len(freqs) array of power.
# Returns the average energy of a sub array.
def get_avg_energy(p_arr):
    ret_list = []
    for t_arr in p_arr:
        ret_list.append(np.average(t_arr))
    return ret_list

#Beautiful taken from http://stackoverflow.com/a/19470773
# modified specgram()
def band_limited_specgram(x, NFFT=256, Fs=2, Fc=0, detrend=mlab.detrend_none,
                          window=mlab.window_hanning, noverlap=128,
                          cmap=None, xextent=None, pad_to=None, sides='default',
                          scale_by_freq=None, minfreq = None, maxfreq = None, **kwargs):
    """
    call signature::

      specgram(x, NFFT=256, Fs=2, Fc=0, detrend=mlab.detrend_none,
               window=mlab.window_hanning, noverlap=128,
               cmap=None, xextent=None, pad_to=None, sides='default',
               scale_by_freq=None, minfreq = None, maxfreq = None, **kwargs)

    Compute a spectrogram of data in *x*.  Data are split into
    *NFFT* length segments and the PSD of each section is
    computed.  The windowing function *window* is applied to each
    segment, and the amount of overlap of each segment is
    specified with *noverlap*.

    %(PSD)s

      *Fc*: integer
        The center frequency of *x* (defaults to 0), which offsets
        the y extents of the plot to reflect the frequency range used
        when a signal is acquired and then filtered and downsampled to
        baseband.

      *cmap*:
        A :class:`matplotlib.cm.Colormap` instance; if *None* use
        default determined by rc

      *xextent*:
        The image extent along the x-axis. xextent = (xmin,xmax)
        The default is (0,max(bins)), where bins is the return
        value from :func:`mlab.specgram`

      *minfreq, maxfreq*
        Limits y-axis. Both required

      *kwargs*:

        Additional kwargs are passed on to imshow which makes the
        specgram image

      Return value is (*Pxx*, *freqs*, *bins*, *im*):

      - *bins* are the time points the spectrogram is calculated over
      - *freqs* is an array of frequencies
      - *Pxx* is a len(times) x len(freqs) array of power
      - *im* is a :class:`matplotlib.image.AxesImage` instance

    Note: If *x* is real (i.e. non-complex), only the positive
    spectrum is shown.  If *x* is complex, both positive and
    negative parts of the spectrum are shown.  This can be
    overridden using the *sides* keyword argument.

    **Example:**

    .. plot:: mpl_examples/pylab_examples/specgram_demo.py

    """

    #####################################
    # modified  axes.specgram() to limit
    # the frequencies plotted
    #####################################

    # this will fail if there isn't a current axis in the global scope
    ax = plt.gca()
    Pxx, freqs, bins = mlab.specgram(x, NFFT, Fs, detrend,
         window, noverlap, pad_to, sides, scale_by_freq)

    # modified here
    #####################################
    if minfreq is not None and maxfreq is not None:
        Pxx = Pxx[(freqs >= minfreq) & (freqs <= maxfreq)]
        freqs = freqs[(freqs >= minfreq) & (freqs <= maxfreq)]
    #####################################

    Z = 10. * np.log10(Pxx)
    Z = np.flipud(Z)

    if xextent is None: xextent = 0, np.amax(bins)
    xmin, xmax = xextent
    freqs += Fc
    extent = xmin, xmax, freqs[0], freqs[-1]
    im = ax.imshow(Z, cmap, extent=extent, **kwargs)
    ax.axis('auto')

    return Pxx, freqs, bins, im



# Have colormaps separated into categories:
# Taken from http://matplotlib.org/examples/color/colormaps_reference.html

cmaps = [('Perceptually_Uniform_Sequential',
                            ['viridis', 'inferno', 'plasma', 'magma']),
         ('Sequential',     ['Blues', 'BuGn', 'BuPu',
                             'GnBu', 'Greens', 'Greys', 'Oranges', 'OrRd',
                             'PuBu', 'PuBuGn', 'PuRd', 'Purples', 'RdPu',
                             'Reds', 'YlGn', 'YlGnBu', 'YlOrBr', 'YlOrRd']),
         ('Sequential(2)', ['afmhot', 'autumn', 'bone', 'cool',
                             'copper', 'gist_heat', 'gray', 'hot',
                             'pink', 'spring', 'summer', 'winter']),
         ('Diverging',      ['BrBG', 'bwr', 'coolwarm', 'PiYG', 'PRGn', 'PuOr',
                             'RdBu', 'RdGy', 'RdYlBu', 'RdYlGn', 'Spectral',
                             'seismic']),
         ('Qualitative',    ['Accent', 'Dark2', 'Paired', 'Pastel1',
                             'Pastel2', 'Set1', 'Set2', 'Set3']),
         ('Miscellaneous',  ['gist_earth', 'terrain', 'ocean', 'gist_stern',
                             'brg', 'CMRmap', 'cubehelix',
                             'gnuplot', 'gnuplot2', 'gist_ncar',
                             'nipy_spectral', 'jet', 'rainbow',
                             'gist_rainbow', 'hsv', 'flag', 'prism'])]

# Returns a generator that returns color strings for the form "categorySPACEcmap"
def get_color_maps():
    for color_tup in cmaps:
        category = color_tup[0]
        colors = color_tup[1]
        for color in colors:
            yield category + ' ' + color

# This expects a string returned by get_color_maps
def get_cm_color_enum(map_string):
    color = map_string.split(' ')[1]
    return plt.get_cmap(color)

