# -*- coding: utf-8 -*-

import subprocess

import numpy as np
import matplotlib.pylab as pl

from matplotlib.ticker import AutoLocator, FuncFormatter, MultipleLocator
from matplotlib.widgets import Button
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm
from matplotlib.colorbar import ColorbarBase

import c5.data


class SelectXRange:
    def __init__(self, fig, f):
        self.fig = fig
        self.func = f
        self.click = fig.canvas.mpl_connect('button_press_event', self.on_click)
        self.release = fig.canvas.mpl_connect('button_release_event', self.on_release)
        self.a = None
        self.pos = None        
        #self.press = fig.canvas.mpl_connect('key_release_event', self.on_press)
        #self.draw = fig.canvas.mpl_connect('draw_event', self.on_draw)        

    def on_click(self, event):
        if event.button != 1: return
        if pl.get_current_fig_manager().toolbar.mode != '': return    
        self.a = event.xdata
        self.pos = event.x

    def on_release(self, event):
        if (event.button != 1) or (self.a is None) : return
        if abs(self.pos - event.x) < 10: return
        self.func(min(self.a,event.xdata),max(self.a,event.xdata))
        self.a = None
        self.pos = None    

class _PlotPlayer:
    def __init__(self, data, filename, offset):
        self.timestamps = data[:]['timestamp']
        self.ydata = []
        for i in data.dtype.names:
            if i == 'timestamp': continue
            if i == 'delta': continue
            self.ydata.append(data[:][i])
        self.duration = self.timestamps[-1] - self.timestamps[0]
        self.duration /= 1000.0
        self.start = (self.timestamps[0]-offset)/1000.0
        if ".wav" in filename:
            f = scikits.audiolab.Sndfile(filename,'r')
            skips =  self.start * f.samplerate
            skips = int(skips)
            while (skips > 0):
                read = min(100000,skips)
                f.read_frames(read)
                skips -= read
            self.sample = f.read_frames(int(self.duration * f.samplerate)).transpose()
            f.close()
        else: self.sample = None
        self.call = ['mplayer','-ss',str(self.start),'-endpos',str(self.duration),filename]

    def show(self):
        sets = len(self.ydata)
        self.fig = pl.figure()
        if self.sample is not None:
            ax = self.fig.add_subplot(sets+2,1,1)
            d1 = c5.data.resample(self.sample[0,:], self.timestamps.shape[0])
            ax.plot(self.timestamps, np.abs(d1))
            if self.sample.shape[1] > 1:
                d2 = c5.data.resample(self.sample[1,:], self.timestamps.shape[0])
                ax.plot(self.timestamps, np.abs(d2)*-1)
                ax.set_xlim(self.timestamps[0],self.timestamps[-1])
        for i in range(sets+1):
            ax = self.fig.add_subplot(sets+2,1,i+2)
            ax.set_xlim(self.timestamps[0],self.timestamps[-1])
            if i < sets:
                ax.plot(self.timestamps, self.ydata[i])
            else: 
                ax = self.fig.add_subplot(sets+2,1,i+2)
                self.bplay = Button(ax, 'Play')
                self.bplay.on_clicked(self.play)
        self.fig.show()
        
    def play(self, event):
        print self.call
        self.thread = c5.data.WorkerThread(subprocess.call,self.call)
        self.thread.start()
#        self.thread2 = c5.data.WorkerThread(self.moving_lines)
#        self.thread2.start()
#        
#    def moving_lines(self):
#        try:
#            lines = []
#            t = self.timestamps[0]
#            for ax in self.fig.get_axes()[:-1]:
#                line = ax.axvline(color='r')
#                lines.append(line)
#            while ((t < self.timestamps[-1]) and (self.fig.number in pl.get_fignums())):
#                print t                
#                for line in lines:
#                    line.set_xdata(t)
#                    time.sleep()
#                t += 1000
#                pl.draw()
#            del lines
#            del self.thread
#        except Exception as e:
#            print e.message

class PlotPlayer:
    def __init__(self, filename, data):
        self.filename = filename
        self.data = data
    def show_range(self, x, y):
        d = self.data[(self.data[:]['timestamp'] >= x) & (self.data[:]['timestamp'] <= y)]
        player = _PlotPlayer(d, self.filename,self.data[0]['timestamp'])
        player.show()
        
def _time_formater(x, pos):
    # just returns minutes
    return '%02d:%02d' % ((x % 3600000) / 60000, (x % 60000) / 1000.0)
   #return '%02d:%02d:%05.2f' % (x / 3600000, (x % 3600000) / 60000, (x % 60000) / 1000.0)

def format_time(ax=None, ticks=None, rotation=None):
  if ax is None:
    ax = pl.gca().get_xaxis()
  if ticks is None:
    majorLocator = AutoLocator()
  else:
    majorLocator = MultipleLocator(ticks)
  majorFormatter = FuncFormatter(_time_formater)
  ax.set_major_locator(majorLocator)
  ax.set_major_formatter(majorFormatter)
  if rotation:
    for label in ax.get_ticklabels(): 
       label.set_rotation(rotation)

def ms2date(timestamps):
    dts = map(pl.datetime.fromtimestamp, timestamps/1000.0)    
    return pl.date2num(dts) - 0.036

# Topics: line, color, LineCollection, cmap, colorline, codex
# http://nbviewer.ipython.org/github/dpsanders/matplotlib-examples/blob/master/colorline.ipynb
'''
Defines a function colorline that draws a (multi-)colored 2D line with coordinates x and y.
The color is taken from optional data in z, and creates a LineCollection.

z can be:
- empty, in which case a default coloring will be used based on the position along the input arrays
- a single number, for a uniform color [this can also be accomplished with the usual plt.plot]
- an array of the length of at least the same length as x, to color according to this data
- an array of a smaller length, in which case the colors are repeated along the curve

The function colorline returns the LineCollection created, which can be modified afterwards.

See also: plt.streamplot
'''
# Data manipulation:

def make_segments(x, y):
    '''
    Create list of line segments from x and y coordinates, in the correct format for LineCollection:
    an array of the form   numlines x (points per line) x 2 (x and y) array
    '''

    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    
    return segments


# Interface to LineCollection:
#http://nbviewer.ipython.org/github/dpsanders/matplotlib-examples/blob/master/colorline.ipynb
def colorline(x, y, z=None, cmap=pl.get_cmap('copper'), norm=pl.Normalize(0.0, 1.0), linewidth=3, alpha=1.0):
    '''
    Plot a colored line with coordinates x and y
    Optionally specify colors in the array z
    Optionally specify a colormap, a norm function and a line width
    '''
    
    # Default colors equally spaced on [0,1]:
    if z is None:
        z = np.linspace(0.0, 1.0, len(x))
           
    # Special case if a single number:
    if not hasattr(z, "__iter__"):  # to check for numerical input -- this is a hack
        z = np.array([z])
        
    z = np.asarray(z)
    
    segments = make_segments(x, y)
    lc = LineCollection(segments, array=z, cmap=cmap, norm=norm,
                        linewidth=linewidth, alpha=alpha)

    ax = pl.gca()
    ax.add_collection(lc)
    ax1 = pl.gcf().add_axes([0.95, 0.2, 0.05, 0.6])
    cb1 = ColorbarBase(ax1, cmap=cmap, norm=norm,
                                  orientation='vertical')
    return lc


def clear_frame(ax=None):
    # Taken from a post by Tony S Yu
    if ax is None:
        ax = pl.gca()
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)
    for spine in ax.spines.itervalues():
        spine.set_visible(False)

def axis_colorplot(m, ps, **kwargs):
    ax = pl.gca()
    ax.set_xticks(np.arange(ps.shape[1])+0.5, minor=False)
    ax.set_yticks(np.arange(ps.shape[0])+0.5, minor=False)
    # want a more natural, table-like display
    ax.invert_yaxis()
    ax.xaxis.tick_top()
    ax.set_xticklabels(sorted(m), minor=False)
    ax.set_yticklabels(sorted(m), minor=False)
    t = pl.pcolor(ps, alpha=0.8, edgecolor='k', **kwargs)
    t = pl.colorbar()
