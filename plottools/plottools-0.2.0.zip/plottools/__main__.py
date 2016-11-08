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
import color.colorscheme
import color.default
import matplotlib.pyplot as plt

if 'cst' in sys.argv:
    print('Starting Color Scheme Tool')
    cst = color.colorscheme.ColorschemeTool(color.default.colors)
    
if 'cs' in sys.argv:
    print('Plotting the default Color Scheme')
    color.default.plot()
    plt.show()