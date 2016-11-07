import os

# Changes working directory to /data to access datasets
os.chdir("../data/")

'''
a_run_01 = np.genfromtxt('a_run_01.txt')
a_run_02 = np.genfromtxt('a_run_02.txt')
a_run_03 = np.genfromtxt('a_run_03.txt')

def plotter(data):
    time = data[:, 2]
    volt = data[:, 0] # This is in mV

    plt.plot(time, volt, 'bo')
    plt.show()

plotter(a_run_02)
# (1.662 / 0.16754) do this afterwards
'''

import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import matplotlib.cbook as cbook
import numpy as np

data = np.genfromtxt('he_below_l_a_run_02.txt')

def fmt(x, y):
    return 'x: {x:0.6f}\ny: {y:0.6f}'.format(x = x, y = y)

class DataCursor(object):
    # http://stackoverflow.com/a/4674445/190597
    """A simple data cursor widget that displays the x,y location of a
    matplotlib artist when it is selected."""
    def __init__(self, artists, x = [], y = [], tolerance = 5, offsets = (20, 20),
                 formatter = fmt, display_all = False):
        """Create the data cursor and connect it to the relevant figure.
        "artists" is the matplotlib artist or sequence of artists that will be 
            selected. 
        "tolerance" is the radius (in points) that the mouse click must be
            within to select the artist.
        "offsets" is a tuple of (x,y) offsets in points from the selected
            point to the displayed annotation box
        "formatter" is a callback function which takes 2 numeric arguments and
            returns a string
        "display_all" controls whether more than one annotation box will
            be shown if there are multiple axes.  Only one will be shown
            per-axis, regardless. 
        """
        self._points = np.column_stack((x,y))
        self.formatter = formatter
        self.offsets = offsets
        self.display_all = display_all
        if not cbook.iterable(artists):
            artists = [artists]
        self.artists = artists
        self.axes = tuple(set(art.axes for art in self.artists))
        self.figures = tuple(set(ax.figure for ax in self.axes))

        self.annotations = {}
        for ax in self.axes:
            self.annotations[ax] = self.annotate(ax)

        for artist in self.artists:
            artist.set_picker(tolerance)
        for fig in self.figures:
            fig.canvas.mpl_connect('pick_event', self)

    def annotate(self, ax):
        """Draws and hides the annotation box for the given axis "ax"."""
        annotation = ax.annotate(self.formatter, xy = (0, 0), ha = 'right',
                xytext = self.offsets, textcoords = 'offset points', va = 'bottom',
                bbox = dict(boxstyle = 'round,pad=0.5', fc = 'yellow', alpha = 0.5),
                arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3,rad=0')
                )
        annotation.set_visible(False)
        return annotation

    def snap(self, x, y):
        """Return the value in self._points closest to (x, y).
        """
        idx = np.nanargmin(((self._points - (x,y))**2).sum(axis = -1))
        return self._points[idx]
    def __call__(self, event):
        """Intended to be called through "mpl_connect"."""
        # Rather than trying to interpolate, just display the clicked coords
        # This will only be called if it's within "tolerance", anyway.
        x, y = event.mouseevent.xdata, event.mouseevent.ydata
        annotation = self.annotations[event.artist.axes]
        if x is not None:
            if not self.display_all:
                # Hide any other annotation boxes...
                for ann in self.annotations.values():
                    ann.set_visible(False)
            # Update the annotation in the current axis..
            x, y = self.snap(x, y)
            annotation.xy = x, y
            annotation.set_text(self.formatter(x, y))
            annotation.set_visible(True)
            event.canvas.draw()

x = data[:, 2]
y = data[:, 0] # This is in mV

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
scat = ax.scatter(x, y)
DataCursor(scat, x, y)
plt.show()