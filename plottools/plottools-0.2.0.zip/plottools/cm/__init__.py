#!/usr/bin/python
################################################################################
#    Copyright 2015 Brecht Baeten
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
import numbers
import numpy as np

from hotwater import test_cm as hotwater
from coldhot import test_cm as coldhot
from hue import test_cm as hue

def cm_to_svg(colormap,filename,stops=3):
    """
    creates a svg file with the colormap defined as a gradient
    
    Arguments:
        colormap:     a matplotlib colormap instance
        filename:     string, the file to write the svg file to
        stops=3:    int or list fo floats, number of stops to use in the gradient or the position of the stops in the range of 0.0 to 1.0
    
    Example:
        plottools.cm.cm_to_svg(plottools.cm.hotwater,'hotwater.svg',stops=5)
    """
    
    # input handling
    if isinstance(stops, numbers.Number):
        stops = np.linspace(0.0,1.0,max(2,stops))
    
    
    # get the colors of the colormap at the stops
    colors = ['#{:02x}{:02x}{:02x}'.format(int(colormap(s)[0]*255),int(colormap(s)[1]*255),int(colormap(s)[2]*255)) for s in stops]

    
    # current path
    modulepath = os.path.dirname(sys.modules[__name__].__file__)

    # open the cm_blank svg file
    blank_file = open(os.path.join(modulepath,'cm_blank.svg'), 'r') 
    content = blank_file.read()
    blank_file.close()

    # find the index where the stops must come
    ind = content.find('    </linearGradient>')
    before = content[:ind]
    after = content[ind:]
    
    new_content = before
    for s,c in zip(stops,colors):
        new_content = new_content + '      <stop id="stop{:04.0f}" offset="{:.3f}" style="stop-color:{};stop-opacity:1;" />\n'.format(s*1000,s,c)

    new_content = new_content+after
    
    new_file = open(filename, 'w')
    new_file.write(new_content)
    new_file.close()