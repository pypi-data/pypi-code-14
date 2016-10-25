from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from .airports import Airports
from .misc import Images, Files
from .teapot import Teapot
from .topography import Topography
from .wolfpass import Wolfpass

try:
    del airports, misc, teapot, topography, wolfpass
    del base
    del absolute_import, division, print_function, unicode_literals
except NameError:
    # Error cleaning namespace
    pass
