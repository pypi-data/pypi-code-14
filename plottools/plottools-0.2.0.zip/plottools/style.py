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
 
         
def horizontalgrid(axes=None):
    """
    Sets a style with a horizontal grid to the axes
    
    Parameters
    ----------
    axes : matplotlib axes object
        the axes to which to apply the style, if omitted the current axis 
        obtained with plt.gca() it styled
            
    Examples
    --------
    .. plot::
    
        >>> import matplotlib.pyplot as plt
        >>> import numpy as np
        >>> import plottools
        >>> plt.plot(np.arange(10),10*np.random.random(10))
        >>> plottools.style.horizontalgrid()
        >>> plt.show()
    
    """
    
    if axes == None:
        axes = plt.gca()
        
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

    
def noxticks(axes=None):
    """
    Sets a style with no ticks on the x axis
    
    Parameters
    ----------
    axes : matplotlib axes object
        the axes to which to apply the style, if omitted the current axis 
        obtained with plt.gca() it styled
            
    Examples
    --------
    .. plot::
    
        >>> import matplotlib.pyplot as plt
        >>> import numpy as np
        >>> import plottools
        >>> plt.plot(np.arange(10),10*np.random.random(10))
        >>> plottools.style.noxticks()
        >>> plt.show()
    
    """
    if axes == None:
        axes = plt.gca()

    axes.xaxis.set_tick_params(which='both', bottom='off', top='off', left='off', right='off', labelbottom='on', labelleft='on')
    
    
def set(*style,**kwargs):
    """
    Sets styles of a single axes object
    
    Parameters
    ----------
    style : string or list of strings
        style string, if a list is supplied all styles in the list are applied
        
    axes : matplotlib axes object
        the axes to which to apply the style, if omitted the current axis 
        obtained with plt.gca() it styled
        
    Examples
    --------
    .. plot::
    
        >>> import matplotlib.pyplot as plt
        >>> import numpy as np
        >>> import plottools
        >>> plt.plot(np.arange(10),10*np.random.random(10))
        >>> plottools.style.set(['horizontalgrid','noxticks'])
        >>> plt.show()
    
    """
    
    if not 'axes' in kwargs:
        axes = plt.gca()
    else:
        axes = kwargs['axes']
        
    #if isinstance(style, basestring):
    #    style = [style]
        
    for s in style:
        if s in ['horizontalgrid','horizontalgridwithoutticks']:
            horizontalgrid(axes)
        
        if s in ['noxticks','horizontalgridwithoutticks']:
            noxticks(axes)
            
         
         
        