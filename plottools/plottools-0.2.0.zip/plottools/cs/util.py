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

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from colorspacious import cspace_converter  
from PIL import Image

    
    
def plot_colors(ax,colors,order=None):

    if order == None:
        order = colors.keys()
    elif order == 'J':
        order = order_by_J(colors)
        
    for i,key in enumerate(order):
        ax.add_patch(  patches.Rectangle( (i, 0), 1.0, 1.0, facecolor=colors[key], edgecolor='none') )
        ax.text(i+0.5,0.5,key,ha='center')
        
    plt.xlim([0,len(colors)])
    plt.ylim([0,1])


# derived from matplotlib viscm
_sRGB1_to_JCh = cspace_converter('sRGB1', 'JCh')
_JCh_to_sRGB1 = cspace_converter('JCh', 'sRGB1')

def to_greyscale(sRGB1):
    JCh = _sRGB1_to_JCh(sRGB1)
    JCh[..., 1] = 0
    return _JCh_to_sRGB1(JCh)
    

def change_lightness_to_match_greyscale(col,grey):
    JCh = _sRGB1_to_JCh(col)
    Js = np.linspace(1e-6,100,20)
    gs = []
    
    for Ji in Js:
        JCh[..., 0] = Ji
        RGBi = _JCh_to_sRGB1(JCh)
        RGBi = np.clip(RGBi,0,1)
        gi = np.mean(to_greyscale(RGBi))
        
        gs.append(gi)

    J = np.interp(grey,gs,Js)
    JCh[..., 0] = J
    newcol = _JCh_to_sRGB1( JCh )
    newcol = np.clip(newcol,0,1)

    return newcol

def order_by_J(colors):
    keys = colors.keys()
    J = [_sRGB1_to_JCh(colors[key])[0] for key in keys]
    order = [k for (j,k) in sorted(zip(J,keys))]
    
    return order
    
def prepare_print_scan(colors):
    
    order = order_by_J(colors)
    
    colors_grey = {}

    for key,val in colors.items():
        colors_grey[key] = to_greyscale(val)

    fig = plt.figure(figsize=(16./2.54,24./2.54))
    ax1 = fig.add_subplot(211)
    plot_colors(ax1,colors,order)
    plt.title('print color')

    ax2 = fig.add_subplot(212)
    plot_colors(ax2,colors_grey,order)  
    plt.title('print greyscale')


def analyse_print_scan(scanfile,colors):

    im = Image.open(scanfile).convert('RGB')

    # order the colors according to lightness
    keys = colors.keys()
    J = [_sRGB1_to_JCh(colors[key])[0] for key in keys]
    order = [k for (j,k) in sorted(zip(J,keys))]

    width,height = im.size

    scan_colors = {}
    scan_colors_grey = {}
    for i,key in enumerate(order):
        # get the colors from the scan file
        x = int(0.20*width + 0.66*i/len(order)*width)

        y = int(0.25*height)
        r = [ im.getpixel( (xi, yi) )[0] for xi in np.array(x)+np.arange(-int(0.02*width),int(0.02*width)) for yi in np.array(y)+np.arange(-int(0.02*height),int(0.02*height)) ]
        g = [ im.getpixel( (xi, yi) )[1] for xi in np.array(x)+np.arange(-int(0.02*width),int(0.02*width)) for yi in np.array(y)+np.arange(-int(0.02*height),int(0.02*height)) ]
        b = [ im.getpixel( (xi, yi) )[2] for xi in np.array(x)+np.arange(-int(0.02*width),int(0.02*width)) for yi in np.array(y)+np.arange(-int(0.02*height),int(0.02*height)) ]
        

        scan_colors[key] = (np.mean(r)/255,np.mean(g)/255,np.mean(b)/255)

        y = int(0.80*height)
        r = [ im.getpixel( (xi, yi) )[0] for xi in np.array(x)+np.arange(-int(0.02*width),int(0.02*width)) for yi in np.array(y)+np.arange(-int(0.02*height),int(0.02*height)) ]
        g = [ im.getpixel( (xi, yi) )[1] for xi in np.array(x)+np.arange(-int(0.02*width),int(0.02*width)) for yi in np.array(y)+np.arange(-int(0.02*height),int(0.02*height)) ]
        b = [ im.getpixel( (xi, yi) )[2] for xi in np.array(x)+np.arange(-int(0.02*width),int(0.02*width)) for yi in np.array(y)+np.arange(-int(0.02*height),int(0.02*height)) ]
        
        scan_colors_grey[key] = (np.mean(r)/255,np.mean(g)/255,np.mean(b)/255)


    fig = plt.figure(figsize=(16./2.54,24./2.54))
    ax1 = fig.add_subplot(211)
    plot_colors(ax1,scan_colors,order)
    plt.title('scan color')

    ax2 = fig.add_subplot(212)
    plot_colors(ax2,scan_colors_grey,order)  
    plt.title('scan greyscale')
    
    
    # compare the printed values with to_greyscale
    greyscales = {}
    for key,val in colors.items():
        greyscales[key] = np.mean(to_greyscale(val))

    scan_greyscales= {}
    for key,val in scan_colors.items():
        scan_greyscales[key] = np.mean(val)


    # rescale so first and last value are equal
    x  = np.arange(len(order))
    y1 = np.array([greyscales[key] for key in order])
    y2 = np.array([scan_greyscales[key] for key in order])
    # rescale so first and last value are equal
    y2 = min(y1) + (y2-min(y2))*(max(y1)-min(y1))/(max(y2)-min(y2))

    plt.figure()
    plt.plot([x[0],x[-1]],[y1[0],y1[-1]],'k--')
    
    plt.plot(x,y1,'o',color='b',label='greyscale')
    plt.plot(x,y2,'s',color='r',label='printed')

    for xi,yi,key in zip(x,y1,order):
        plt.text(xi,yi-0.10,key)

    plt.legend(loc='lower right',numpoints=1)
    plt.xlim([-0.5,len(order)-1+0.5])
    plt.ylim([-0.02,1.02])
    