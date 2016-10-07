import numpy as np
import os
import random
import sys
import unittest

from os import path
from unittest.mock import patch, Mock

from test import patch_tecutil

import tecplot as tp
from tecplot.exception import *
from tecplot.constant import *
from tecplot.data.operate import execute_equation
from tecplot.plot import *
from tecplot.legend import ContourLegend, LineLegend
from tecplot.tecutil import IndexRange

from ..sample_data import sample_data

class TestCartesian2DFieldAxes(unittest.TestCase):
    pass

class TestCartesian3DFieldAxes(unittest.TestCase):
    pass

class TestPolarLineAxes(unittest.TestCase):
    pass

class TestXYLineAxes(unittest.TestCase):
    pass
