#!/usr/bin/env/ python
################################################################################
#    Copyright 2016 Brecht Baeten
#    This file is part of plottools.
#    
#    plottools is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#    
#    plottools is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#    
#    You should have received a copy of the GNU General Public License
#    along with plottools.  If not, see <http://www.gnu.org/licenses/>.
################################################################################

import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.widgets import Button, Slider

from cycler import cycler

import util
from .. import cm

################################################################################
# Colorscheme class 
################################################################################
class Colorscheme(object):
    """
    A colorscheme class useful for plotting
   
    """
    
    def __init__(self,colors,longnames=None,cycle=None,base=None):
        """
        defines a colorscheme object useful for plotting
        
        Parameters
        ----------
        colors : dict
            Dictionary of named colors as RGB (0-1) tupples
        
        longnames : dict, optional
            Dictionary of long names of the colors specified in colors
            
        cycle : list, optional
            List with the cycle order
        
        Examples
        --------
        >>> cs = Colorscheme({'r':(1.,0.,0.),'g':(0.,1.,0.),'b':(0.,0.,1.)},['b','g','r'])
        >>> print( cs[0] )
        >>> 
        >>> print( cs.next() )
        >>> print( cs.next() )
        >>> 
        >>> cs.reset_index()
        >>> print( cs.next() )
        """
        
        
        if longnames == None:
            longnames = {k:k for k in colors.keys()}
            
        if cycle == None:
            cycle = colors.keys()
            
            
        self.colors = colors    
        self.longnames = longnames
        self.cycle = cycle
        self.currentindex = 0
        self.base = base
        
        # create light and dark variants
        if base==None:
            lightcolors = {}
            darkcolors = {}
            for key,val in colors.items():
                JCh = util._sRGB1_to_JCh(val)
                JCh[0] = min(JCh[0]+30,100)
                lightcolors[key] = np.clip(util._JCh_to_sRGB1(JCh),0,1)
                
                JCh = util._sRGB1_to_JCh(val)
                JCh[0] = max(JCh[0]-20,1e-6)
                darkcolors[key] = np.clip(util._JCh_to_sRGB1(JCh),0,1)
                
            self.light = Colorscheme(lightcolors,longnames=longnames,cycle=cycle,base=self)
            self.dark = Colorscheme(darkcolors,longnames=longnames,cycle=cycle,base=self)
            
        
    def next(self):
        """
        get the next color in the cycle
        """
        c = self.colors[self.cycle[self.currentindex]]
        self.currentindex += 1
        if self.currentindex >= len(self.cycle):
            self.currentindex = 0
            
        return c
        
    def reset_index(self):
        """
        resets the current color index to 0
        """
        
        self.currentindex = 0
    
    def set_as_default(self):
        """
        sets the colorscheme as the default color cycle in matplotlib figures
        """
        
        plt.rc('axes',prop_cycle=cycler('color', [self.colors[c] for c in self.cycle]) )
    
    def __getitem__(self,key):
        if isinstance(key,int):
            self.currentindex = key+1
            return self.colors[self.cycle[key]]
        else:
            if key in self.longnames:
                key = self.longnames[key]
            
            self.currentindex = self.cycle.index(key)+1
            return self.colors[key]

    def keys(self):
        return self.colors.keys()
        
    def values(self):
        return [self.colors[key] for key in self.keys()]

    def items(self):
        return zip(self.keys(),self.values())
        
    def plot(self,ax=None):
        """
        plots the current colorscheme main colors
        """
        if ax == None:
            fig,ax = plt.subplots()
        
        util.plot_colors(ax,self.colors,order=self.cycle)
        
    def to_svg(self,filename):
        """
        converts the colorscheme to an svg file with block of colors ordered
        according to the cycle
        
        parameters
        ----------
            filename : string
                the file to write the svg file to
         
        Examples
        --------
        >>>> plottools.colors.to_svg('defaultcolors.svg')
        
        """

        # get the colors of the colorscheme
        colors = ['#{:02x}{:02x}{:02x}'.format(int(self.colors[k][0]*255),int(self.colors[k][1]*255),int(self.colors[k][2]*255)) for k in self.cycle]

        width = 100./len(self.cycle)
        x = [i*width for i in range(len(self.cycle))]
        
        # current path
        modulepath = os.path.dirname(sys.modules[__name__].__file__)

        # open the cs_blank svg file
        blank_file = open(os.path.join(modulepath,'cs_blank.svg'), 'r') 
        content = blank_file.read()
        blank_file.close()

        # find the rectangle template
        ind0 = content.find('    <rect')
        ind1 = content.find('  </g>')
        before = content[:ind0]
        after = content[ind1:]
        
        
        new_content = before
        for k,c,x in zip(self.cycle,colors,x):
            new_content = new_content + '    <rect\n       style="opacity:1;fill:{};fill-opacity:1;stroke:none;"\n       id="colorRectangle_{}"\n       width="{}"\n       height="100"\n       x="{}"\n       y="0" />\n'.format(c,k,width,x)

        new_content = new_content+after
        
        new_file = open(filename, 'w')
        new_file.write(new_content)
        new_file.close()

        
        
        
class ColorschemeTool(object):
    """
    """
    def __init__(self,colorscheme):
        """
        """
            
        if colorscheme.__class__ == Colorscheme:
            colors = colorscheme.colors
        else:
            colors = colorscheme
            
        self.order = util.order_by_J(colors)
        self.RGB = colors
        self.grey = self._to_greyscale(colors)
        self.exampledata = self._generate_exampledata(self.order)
        
        
        plt.figure(figsize=(12,10))
        axcolor = 'None'
        
        x = 0.70
        y = 0.40
        w = 0.10
        h = 0.50
        
        self.ax_col = plt.axes([x, y, w, h])
        self.ax_col.get_xaxis().set_visible(False)
        self.ax_col.get_yaxis().set_visible(False)
        
        self.ax_grey = plt.axes([x+w+0.05, y, w, h])
        self.ax_grey.get_xaxis().set_visible(False)
        self.ax_grey.get_yaxis().set_visible(False)
        
        
        self.ax_distribution = plt.axes([0.05, 0.05, 0.45, y-0.10])
        self.ax_example_color = plt.axes([0.55, 0.23, 0.40, 0.12])
        self.ax_example_grey  = plt.axes([0.55, 0.05, 0.40, 0.12])
        
        
        ax_btn_print_rgb = plt.axes([0.70, 0.92, 0.25, 0.05])
        self.btn_print_rgb = Button(ax_btn_print_rgb, 'Print RGB values')
        self.btn_print_rgb.on_clicked(self.print_rgb)
        
        # create initial plots
        self.plot_colors()
        self.plot_distribution()
        self.plot_example()
        
        
        # create JCh sliders
        self.slider_J = {}
        self.slider_C = {}
        self.slider_h = {}
        
        for i,key in enumerate(self.order):
            RGB = self.RGB[key]
            JCh = util._sRGB1_to_JCh(RGB)
            
            # J
            aJ = plt.axes([0.05, y+i*h/len(self.order)+0.02, x-0.15, 0.05])
            aJ.imshow( np.linspace(0, 100, 101).reshape(1, -1), cmap='gray' )
            sJ = Slider(aJ, r'J', 0, 100, valinit=JCh[0])
            sJ.on_changed(self._slider_update)
            
            self.slider_J[key] = sJ
            
            # C
            aC = plt.axes([0.05, y+i*h/len(self.order)+0.00, x-0.15, 0.05])
            aC.imshow( np.linspace(0, 100, 101).reshape(1, -1), cmap='gray' )
            sC = Slider(aC, r'C', 0, 100, valinit=JCh[1])
            sC.on_changed(self._slider_update)
            
            self.slider_C[key] = sC
            
            # h
            ah = plt.axes([0.05, y+i*h/len(self.order)-0.02, x-0.15, 0.05])
            ah.imshow( np.linspace(0, 100, 101).reshape(1, -1), cmap=cm.hue )
            sh = Slider(ah, r'h', 0, 100, valinit=JCh[2]/360.*100.)
            sh.on_changed(self._slider_update)
            
            self.slider_h[key] = sh
            
        plt.show() 
         
    def plot_colors(self):
        
        # clear the axes
        self.ax_col.cla()
        self.ax_grey.cla()
        
        # draw patches
        for i,key in enumerate(self.order):
            self.ax_col.add_patch(  patches.Rectangle( (0, i), 1.0, 1.0, facecolor=self.RGB[key], edgecolor='none') )
            self.ax_col.text(0.5,i+0.5,key,ha='center')
            
            self.ax_grey.add_patch(  patches.Rectangle( (0, i), 1.0, 1.0, facecolor=self.grey[key], edgecolor='none') )
            self.ax_grey.text(0.5,i+0.5,key,ha='center')
        
        
        self.ax_col.set_xlim([0,1])    
        self.ax_col.set_ylim([0,len(self.order)])
        
        self.ax_grey.set_xlim([0,1])    
        self.ax_grey.set_ylim([0,len(self.order)])
        
    def plot_distribution(self):

        self.ax_distribution.cla()
        
        x = np.arange(len(self.order))
        y = np.array([ np.mean(util.to_greyscale(self.RGB[key])) for key in self.order])
        
        # add a line connecting 1st and last point
        self.ax_distribution.plot([x[0],x[-1]],[y[0],y[-1]],'b--')
        
        # add greyscale points
        self.ax_distribution.plot(x,y,'bo',label='greyscale')
        
        # add J points
        j = np.array([ 1.*util._sRGB1_to_JCh(self.RGB[key])[0]/100 for key in self.order])
        self.ax_distribution.plot([x[0],x[-1]],[j[0],j[-1]],'r--')
        self.ax_distribution.plot(x,j,'rs',label='lightness')
        
        # add labels
        for xi,yi,key in zip(x,j,self.order):
            self.ax_distribution.text(xi,yi-0.10,key)
        
        self.ax_distribution.set_xlim([-0.5,len(self.order)-1+0.5])
        self.ax_distribution.set_ylim([0.,1.])
        
        self.ax_distribution.legend(loc='lower right',numpoints=1)
        
        
    def plot_example(self):
    
        self.ax_example_color.cla()
        for key in self.order:
            self.ax_example_color.plot(self.exampledata[key],color=self.RGB[key],linewidth=2,label=key)
        #self.ax_example_color.legend()
        
        self.ax_example_grey.cla()
        for key in self.order:
            self.ax_example_grey.plot(self.exampledata[key],color=self.grey[key],linewidth=2,label=key)
        #self.ax_example_grey.legend()
    
    def print_rgb(self,event):
        print('')
        print('RGB values:')
        for k,c in self.RGB.items():
            print( '\'{}\': ({:>3.0f}./255, {:>3.0f}./255, {:>3.0f}./255),'.format(k,c[0]*255,c[1]*255,c[2]*255))
    
    def _generate_exampledata(self,keys):
        exampledata = {}
        for i,key in enumerate(keys):
            exampledata[key] = np.cumsum(np.random.random(100)-0.5) + i
        return exampledata
        
    def _to_greyscale(self,colors):
        grey = {}
        for key,val in colors.items():
            grey[key] = util.to_greyscale(val)
            
        return grey
        
    def _slider_update(self, val):
        for key in self.order:
            jp = self.slider_J[key].val
            cp = self.slider_C[key].val
            hp = self.slider_h[key].val*360./100.

            self.RGB[key] = np.clip(util._JCh_to_sRGB1([jp,cp,hp]),0,1)
        
        self.grey = self._to_greyscale(self.RGB)

        self.plot_colors()
        self.plot_distribution()
        self.plot_example()
