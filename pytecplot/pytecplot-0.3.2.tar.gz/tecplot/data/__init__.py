"""`Dataset`, `Zone`, `Variable` objects and data access/manipulation.

A `Dataset` consists of a matrix of `Zones <Zone>` and
`Variables <Variable>`. Each `Zone`-`Variable` pair corresponds to a data
object which can always be treated as a 1D array, but which may be
interpreted as 2D or 3D in the case of *ijk*-ordered data.
"""
from . import create, extract, interpolate, operate
from .aux_data import AuxData
from .dataset import Dataset, Variable, Zone, Array
from .load import (load_tecplot, load_tecplot_szl, load_cgns, load_fluent,
                   load_plot3d)
from .save import save_tecplot_ascii, save_tecplot_binary
from .query import probe_at_position
