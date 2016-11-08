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

import matplotlib.pyplot as plt
import numpy as np
import itertools

def set_publication_rc():
    """
    Sets rc parameters for creating plots suitable for publication
    
    Notes
    -----
    The computer modern fonts are not installed by default on windows. But can
    be downloaded at https://sourceforge.net/projects/cm-unicode/
    To use new installed fonts in matplotlib you must delete the font cache file
    located at C:\Users\yourusername\.matplotlib
    
    Examples
    --------
    .. plot::
    
        >>> import matplotlib.pyplot as plt
        >>> import numpy as np
        >>> import plottools
        >>>
        >>> plottools.set_publication_rc()
        >>> plt.plot(np.arange(10),10*np.random.random(10))
        >>> plt.xlabel('x-label')
        >>> plt.ylabel('y-label')
        >>> plt.show()
    
    """
    
    # figure
    plt.rc('figure', autolayout=True, figsize=(80/25.4,50/25.4))
    plt.rc('savefig', format='pdf', dpi=150, bbox='tight', pad_inches=0.02)
    
    # text
    #plt.rc('text', usetex=True)
    
    # font
    plt.rc('font', size=6) 
    plt.rc('font', **{'family':'sans-serif', 'sans-serif':['computer modern sans serif', 'CMU Sans Serif'], 'serif':['computer modern roman', 'CMU Serif']} )

    # axes
    plt.rc('axes', linewidth=0.4, labelsize=8)
    plt.rc('axes.formatter', useoffset=False)
    
    # legend
    plt.rc('legend', fontsize=8, frameon=True)
    
    # lines
    plt.rc('lines', linewidth=0.8,markersize=4)
    
    # patch
    plt.rc('patch', linewidth=0.4, edgecolor=(1.0,1.0,1.0))
    
    # ticks
    plt.rc('xtick.major', size=2, width=0.3, pad=3)
    plt.rc('ytick.major', size=2, width=0.3, pad=3)
    plt.rc('xtick.minor', size=1, width=0.3, pad=3)
    plt.rc('ytick.minor', size=1, width=0.3, pad=3)
    
    
def savefig(filename,width=None,height=None,ratio=8./5.,**kwargs):
    """
    Creates a new figure with a specified width and 8:5, width:height ratio
    
    If no width or height are specified a 8cm x 5cm figure is saved. If the
    width and height are specified, a figure of that size is saved.
    If one of width or height is specified, the ratio is used to define the 
    other.
    
    Parameters
    ----------
    width : number
        figure width in cm
        
    height : number
        figure height in cm
        
    ratio : number
        figure height in cm
        
    """
    
    if width is None and height is None:
        width = 8.
        height = width/ratio
    elif not width is None and height is None:
        height = width/ratio
    elif not height is None and width is None:
        width = height*ratio
        
        
    plt.gcf().set_size_inches(width/2.54,height/2.54)
    plt.savefig(filename,**kwargs)
    
    
def set_style(style,axes=None):
    """
    Sets the style of a single axes object from some specification on top of other rc parameters
    
    Parameters
    ----------
    style : {'horizontalgrid','horizontalgridwithoutticks'}
        style string 'horizontalgrid','horizontalgridwithoutticks'
        
    axes : matplotlib axes object
        the axes to which to apply the style, if omitted the current axis 
        obtained with plt.gca() it styled
        
    Examples
    --------
    >>> plt.plot(np.arange(10),10*np.random.random(10))
    >>> plottools.set_style('horizontalgrid')
    >>> plt.show()
    
    """
    
    if axes == None:
        axes = plt.gca()
        
    if style in ['horizontalgrid','horizontalgridwithoutticks']:
        # hide the spines except the bottom one
        axes.spines['top'].set_visible(False)
        # axes.spines['bottom'].set_visible(False)
        axes.spines['right'].set_visible(False)
        axes.spines['left'].set_visible(False)

        # show ticks only on the left bottom  
        axes.get_xaxis().tick_bottom()
        axes.get_yaxis().tick_left()
        
        # add horizontal lines
        yticks = axes.get_yticks()
        xlim = axes.get_xlim()
        
        for y in yticks:
            axes.plot(xlim, [y,y], '-', linewidth=0.3, color='k', alpha=0.3, zorder=-10)
        
        axes.yaxis.set_tick_params(which='both', bottom='off', top='off', labelbottom='on', left='off', right='off', labelleft='on')         
        
        
    if style == 'horizontalgridwithoutticks':
        axes.xaxis.set_tick_params(which='both', bottom='off', top='off', labelbottom='on', left='off', right='off', labelleft='on')
        
                 
              
def zoom_axes(fig,ax,zoom_x,zoom_y,axes_x,axes_y,box=True,box_color='k',box_alpha=0.8,connect=True,connect_color='k',connect_alpha=0.3,spacing=4,tick_width=20,tick_height=12):
    """
    Creates a new axes which zooms in on a part of a given axes.
    
    A box is drawn around the area to be zoomed specified in data coordinates. A
    new empty axes is created at the specified location, supplied in data
    coordinates. The new axis limits are set so that they match the zoom box.
    
    The zoom box and axis can be connected with two lines, connecting the outer 
    most corner points while leaving space for the axis ticks.
   

    Parameters
    ----------
    fig : matplotlib figure
        the figure in which to create a zoom axis
        
    ax : matplotlib axes
        the axis in which to create a zoom axis
        
    zoom_x : list
        [min, max] specifying the zooming horizontal area in data 
        coordinates 
        
    zoom_y : list
        [min, max] specifying the zooming vertical area in data coordinates 
        
    axes_x : list
        [min, max] specifying the new axes horizontal location in data
        coordinates 
    
    axes_y : list
        [min, max] specifying the new axes vertical location in data
        coordinates 
    
    box : bool, optional 
        specifies whether a box is drawn
    
    box_color : color string or tuple,optional 
        specifies the box color
        
    box_alpha : number 
        between 0 and 1, specifies the box alpha   

    connect : bool, optional 
        specifies whether the connecting lines are drawn
    
    connect_color : color string or tuple,optional 
        specifies the connecting lines color
        
    connect_alpha : number 
        between 0 and 1, specifies the connecting lines alpha  
        
    spacing : number
        specifies the spacing between the box, axis and the connecting lines
        in points
    
    tick_width : number
        specifies the width of the tick labels in points to avoid drawing
        connecting lines through the tick labels
    
    tick_height : number
        specifies the height of the tick labels in points to avoid drawing
        connecting lines through the tick labels
            
            
    Returns
    -------
    ax_zoom : matplotlib axes 
        the new axes

    Notes
    -----
    * Axes limits should not be changed after a zoom axes has been added
    * :code:`zoom_axes` does not give the expected results when used on a
      subfigure
    
    Examples
    --------
    .. plot::
    
        >>> import matplotlib.pyplot as plt
        >>> import numpy as np
        >>> import plottools
        >>>
        >>> fig,ax = plt.subplots()
        >>> x = np.linspace(0,1,100)
        >>> y = 1-x + 0.02*(2*np.random.random(len(x))-1)
        >>> ax.plot(x,y)
        >>> ax_zoom = plottools.zoom_axes(fig,ax,[0.1,0.2],[0.8,0.9],[0.6,0.9],[0.6,0.9])
        >>> ax_zoom.plot(x,y)
        >>> plt.show()
    
    """

    plt.tight_layout()
    ax1_p0 = (ax.transData + fig.transFigure.inverted()).transform_point((axes_x[0],axes_y[0]))
    ax1_p1 = (ax.transData + fig.transFigure.inverted()).transform_point((axes_x[1],axes_y[1]))

    ax1 = plt.axes([ax1_p0[0],ax1_p0[1],ax1_p1[0]-ax1_p0[0],ax1_p1[1]-ax1_p0[1]])

    ax1.set_xlim(zoom_x)
    ax1.set_ylim(zoom_y)

    plt.xticks(fontsize=4)
    plt.yticks(fontsize=4)
    ax1.tick_params(axis='x', pad=3)
    ax1.tick_params(axis='y', pad=2)

    if box:
        ax.plot([zoom_x[0],zoom_x[1],zoom_x[1],zoom_x[0],zoom_x[0]],[zoom_y[0],zoom_y[0],zoom_y[1],zoom_y[1],zoom_y[0]],color=box_color,alpha=box_alpha,linewidth=0.4)

    if connect:
        
        # define a box of points of the axes and the zoom
        zoom_xx = [zoom_x[0],zoom_x[0],zoom_x[1],zoom_x[1]]
        zoom_yy = [zoom_y[0],zoom_y[1],zoom_y[1],zoom_y[0]]
        axes_xx = [axes_x[0],axes_x[0],axes_x[1],axes_x[1]]
        axes_yy = [axes_y[0],axes_y[1],axes_y[1],axes_y[0]]
        
        # determine which points to connect
        if axes_x[1] < zoom_x[1]:
            # left
            if axes_y[0] > zoom_y[0]:
                # top
                p1 = 0
                p2 = 2
            elif axes_y[1] < zoom_y[1]:
                # bottom
                p1 = 1
                p2 = 3
            else:
                # center
                p1 = 2
                p2 = 3
        
        elif axes_x[0] > zoom_x[0]:
            # right
            if axes_y[0] > zoom_y[0]:
                # top
                p1 = 1
                p2 = 3
            elif axes_y[1] < zoom_y[1]:
                # bottom
                p1 = 0
                p2 = 2
            else:
                # center
                p1 = 0
                p2 = 1
                
        else:
            # center
            if axes_y[0] > zoom_y[0]:
                # top
                p1 = 0
                p2 = 3
            elif axes_y[1] < zoom_y[1]:
                # bottom
                p1 = 1
                p2 = 2
            else:
                # center, the axes is over the zoom
                p1 = 0
                p2 = 0

        
        line1 = ([zoom_xx[p1],axes_xx[p1]],[zoom_yy[p1],axes_yy[p1]])
        line2 = ([zoom_xx[p2],axes_xx[p2]],[zoom_yy[p2],axes_yy[p2]])
        
       
        # estimate the width and height of the ticks
        tick_width  = (ax.transData.inverted()).transform_point((tick_width,0))[0]-(ax.transData.inverted()).transform_point((0,0))[0]
        tick_height = (ax.transData.inverted()).transform_point((0,tick_height))[1]-(ax.transData.inverted()).transform_point((0,0))[1]
        spacing     = (ax.transData.inverted()).transform_point((spacing,0))[0]-(ax.transData.inverted()).transform_point((0,0))[0]
        
        # create fictional boxes around the axes where no lines should be
        box_axes_x = [ axes_x[0]-tick_width , axes_x[1]+spacing]
        box_axes_y = [ axes_y[0]-tick_height , axes_y[1]+spacing]
        
        box_zoom_x = [ zoom_x[0]-spacing , zoom_x[1]+spacing]
        box_zoom_y = [ zoom_y[0]-spacing , zoom_y[1]+spacing]
        

        
        # cut the lines inside the boxes
        t = np.linspace(0,1,100)
        
        line1_cut = line1
        line2_cut = line2
        for tt in t:
            x = line1[0][0]*(1-tt) + line1[0][1]*tt
            y = line1[1][0]*(1-tt) + line1[1][1]*tt
            if x <= box_zoom_x[0] or x >= box_zoom_x[1] or y <= box_zoom_y[0] or y >= box_zoom_y[1]:
                line1_cut[0][0] = x
                line1_cut[1][0] = y
                break
        
        for tt in t[::-1]:
            x = line1[0][0]*(1-tt) + line1[0][1]*tt
            y = line1[1][0]*(1-tt) + line1[1][1]*tt
            if (x <= box_axes_x[0] or x >= box_axes_x[1]) or (y <= box_axes_y[0] or y >= box_axes_y[1]):
                line1_cut[0][1] = x
                line1_cut[1][1] = y
                break
        
        for tt in t:
            x = line2[0][0]*(1-tt) + line2[0][1]*tt
            y = line2[1][0]*(1-tt) + line2[1][1]*tt
            if (x <= box_zoom_x[0] or x >= box_zoom_x[1]) or (y <= box_zoom_y[0] or y >= box_zoom_y[1]):
                line2_cut[0][0] = x
                line2_cut[1][0] = y
                break
        
        for tt in t[::-1]:
            x = line2[0][0]*(1-tt) + line2[0][1]*tt
            y = line2[1][0]*(1-tt) + line2[1][1]*tt
            if (x <= box_axes_x[0] or x >= box_axes_x[1]) or (y <= box_axes_y[0] or y >= box_axes_y[1]):
                line2_cut[0][1] = x
                line2_cut[1][1] = y
                break
                 
        # draw the connecting lines         
        ax.plot(line1_cut[0],line1_cut[1],color=connect_color,alpha=connect_alpha,linewidth=0.4)
        ax.plot(line2_cut[0],line2_cut[1],color=connect_color,alpha=connect_alpha,linewidth=0.4)
        

    return ax1


    
    
def categorized_xticklabels(xticks,xticklabels,xticklabelnames=None,fmt=None,size=None,rotation=None,spacing=1.4):
    """
    Creates categorized ticks on the x-axis
    
    Parameters
    ----------
    xticks : array-like
        The x-locations of the data points
        
    xticklabels : list of array-likes
        A list of lists or arrays of which each must have the same length as
        xticks. These are all used as x-tick labels, the first array is
        displayed highest, the next arrays are printed below the previous
        one. Results are the most appealing if the 1st array has the highest
        variation and the last array the lowest.
    
    xticklabelnames: list of strings, optional
        A list of names for the labels. It must have the same length as the
        xticklabels list.
     
    fmt: list of fromat strings, optional
        A list of fromatting strings as used by :code:`format` for the tick
        labels. It must have the same length as the xticklabels list.
        
    size: list of numbers, optional
        A list of numbers specifying the size of the ticklabels in points. 
        It must have the same length as the xticklabels list.

    rotation: list of numbers, optional
        A list of numbers specifying the rotation of the ticklabels in
        degrees. It must have the same length as the xticklabels list.  
        
    spacing: number, optional
        Controls the vertical spacing between the differnt ticklabels
            
    Examples
    --------
    .. plot::
    
        >>> import matplotlib.pyplot as plt
        >>> import numpy as np
        >>> import plottools
        >>> 
        >>> plottools.set_publication_rc()
        >>> 
        >>> # generate data
        >>> C,B,A = np.meshgrid([10,20],[0.4,0.6,0.8],[1,2,3],indexing='ij')
        >>> xticklabels = [ A.reshape((-1,)), B.reshape((-1,)), C.reshape((-1,)) ]
        >>> values = [np.random.random(len(t)) for t in xticklabels]
        >>> xticks = np.arange(len(values[0]))
        >>> 
        >>> xticklabelnames = ['coord','$B_\mathrm{value}$','CCC']
        >>> labels = ['set1','set2','set3']
        >>> fmt = ['${:.2f}$','${}$ m','$10^{{{:.0f}}}$']
        >>> rotation = [70,0,0]
        >>> 
        >>> # create the figure
        >>> plt.figure()
        >>> bottom = np.zeros_like(values[0])
        >>> for val,lab in zip(values,labels):
        ...     plt.bar(xticks+0.05,val,0.9,bottom=bottom,label=lab,color=plottools.color.default.next())
        ...     bottom += val
        ...
        >>> 
        >>> plt.legend(framealpha=0.7,loc='upper right')
        >>> plt.ylabel('y-label')
        >>>
        >>> # add categories on the x-axis
        >>> plottools.categorized_xticklabels(xticks+0.5,xticklabels,xticklabelnames=xticklabelnames,fmt=fmt,rotation=rotation)
        >>> plt.show()
    
    """
    
    # input parsing
    if xticklabelnames == None:
        xticklabelnames = ['']*len(xticklabels)
    
    if fmt == None:
        fmt = ['{}']*len(xticklabels)

    if size == None:
        size = [plt.gca().xaxis.get_major_ticks()[0].label.get_fontsize()]*len(xticklabels)
        
    if rotation == None:
        rotation = [0]*len(xticklabels)

    
    dxticks = np.zeros_like(xticks)
    for i in range(len(xticks)-1):
        dxticks[i] = xticks[i+1]-xticks[i]
    dxticks[-1] = dxticks[-2]
    
    # set the x limits
    plt.xlim([xticks[0]-dxticks[0]/2,xticks[-1]+dxticks[-1]/2])
    
    # get both axis limits
    xlim = plt.xlim()
    ylim = plt.ylim()
    
    
    
    # create a list of y positions in points
    yp = []
    ypi = -1

    for i in range(len(xticklabels)):
        ypi += -spacing*size[i] - 1*size[i]*np.sin(1.*rotation[i]/180*np.pi)
        yp.append( ypi )

    # manual xticks and labels
    plt.xticks([])
    
    linepositions = []    
    for i in range(len(xticklabels)-1,0,-1):
        c = xticklabels[i]
        xtick_old = None
        xticklabel_old = None

        for j,xtl in enumerate(c):
            if not xtl == xticklabel_old:
                
                if not j in linepositions:
                    # add the separator line
                    plt.annotate('',xy=(xticks[j]-0.5*dxticks[j], ylim[0]), xycoords='data',xytext=(0, yp[i]), textcoords='offset points',arrowprops={'arrowstyle':'-','color':(0.3,0.3,0.3)})
                    linepositions.append(j)
                    
                if not xticklabel_old==None:
                    # add the tick label
                    xtick_avg = 0.5*(xtick_old - 0.5*dxticks[j]) + 0.5*(xticks[j] - 0.5*dxticks[j])
                    try:
                        lab = fmt[i].format(xticklabel_old)
                    except:
                        lab = xticklabel_old
                    plt.annotate(lab,xy=(xtick_avg, ylim[0]), xycoords='data',xytext=(0, yp[i]), textcoords='offset points',ha="center", va="bottom", size=size[i], rotation=rotation[i])
                
                xtick_old = xticks[j]
                xticklabel_old = xtl
                    
        # add the final tick label
        j = len(c)-1
        xtick_avg = 0.5*(xtick_old - 0.5*dxticks[j]) + 0.5*(xticks[j] + 0.5*dxticks[j])
        try:
            lab = fmt[i].format(xticklabel_old)
        except:
            lab = xticklabel_old
        plt.annotate(lab,xy=(xtick_avg, ylim[0]), xycoords='data',xytext=(0, yp[i]), textcoords='offset points',ha="center", va="bottom", size=size[i], rotation=rotation[i])
           
    # add the deepest ticklabel
    i = 0
    for j,xtl in enumerate(xticklabels[i]):
        try:
            lab = fmt[i].format(xtl)
        except:
            lab = xtl
        plt.annotate(lab,xy=(xticks[j], ylim[0]), xycoords='data',xytext=(0, yp[i]), textcoords='offset points',ha="center", va="bottom", size=size[i], rotation=rotation[i])
        
    # add the final separator line
    i = len(xticklabels)-1
    j = len(xticklabels[-1])-1
    plt.annotate('',xy=(xticks[j]+0.5*dxticks[j], ylim[0]), xycoords='data',xytext=(0, yp[i]), textcoords='offset points',arrowprops={'arrowstyle':'-','color':(0.3,0.3,0.3)})
    linepositions.append(j)
       
    # add the ticklabelnames
    xp = 3
    for i,l in enumerate(xticklabelnames):
        plt.annotate(l,xy=(xlim[0], ylim[0]), xycoords='data',xytext=(-xp, yp[i]+0.1*size[i]), textcoords='offset points',ha="right", va="bottom", size=size[i])

        
        
def cmapval(v,vmin=0,vmax=1,cmap=None):
    """
    Extracts the color belonging to a value or list of values from a colormap
    
    Parameters
    ----------
    v : float, list, tuple
        the value or values for which to return the colors
        
    vmin : float
        the value corresponding to the first color in the colormap
        
    vmax : float
        the value corresponding to the last color in the colormap
        
    cmap : colormap
        a matplotlib colormap   
    
    Returns
    -------
    hexcolor : string or list of strings
        a html representation of the colors correspoinding to the values
        
    Examples
    --------
    >>> import matplotlib.pyplot as plt
    >>> v = cmapval(0.6)
    '#22a784'
    
    >>> v = cmapval([1000,2000,3000],vmin=100,vmax=3150,cmap=plt.cm.plasma)
    ['#8f0da3', '#e46a5d', '#f7e024']
    
    """
    
    if cmap is None:
        cmap = plt.cm.viridis
        
    extractvalue = False
    if not isinstance(v,(list,tuple)):
        v = [v]
        extractvalue = True
        
    color = cmap( np.interp(v,[vmin,vmax],[0.01,0.99]) )
    hexcolor = map(lambda rgb:'#%02x%02x%02x' % (rgb[0]*255,rgb[1]*255,rgb[2]*255),tuple(color[:,0:-1])) 
    
    if extractvalue:
        hexcolor = hexcolor[0]
        
    return hexcolor


        
def marker(i):
    """
    Default cycle of markers
    
    Parameters
    ----------
    i : int
        an index when the supplied index is too big, the markers are cycled
        
    """
    
    values = ['^','s','<','o','>','*','v','1']
    return values[np.mod(i,len(values))]