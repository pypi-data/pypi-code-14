"""Version information can be obtained via `string <str>` with
`tecplot.__version` or by `namedtuple <collections.namedtuple>` with
`tecplot.version_info`. The underlying |Tecplot 360 EX| installation has its
own version which can be obtained through `tecplot.sdk_version` and
`tecplot.sdk_version_info` attribute.
"""
from collections import namedtuple

from .tecutil import _tecinterprocess

Version = namedtuple('Version', ['major', 'minor', 'revision', 'build'])

version = '0.3.2'
build = '75131'
version_info = Version(*[int(x) for x in version.split('.')], build=build or 0)

sdk_version_info = _tecinterprocess.sdk_version_info
sdk_version = _tecinterprocess.sdk_version
