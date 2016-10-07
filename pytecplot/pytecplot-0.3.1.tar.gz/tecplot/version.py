"""Version information can be obtained via `string <str>` or
`namedtuple <collections.namedtuple>`::

    >>> import tecplot
    >>> print(tecplot.__version__)
    0.3.1
    >>> print(tecplot.version_info)
    Version(major=0, minor=3, revision=1, build='70001')

The underlying |Tecplot 360 EX| installation has its own version which can be
obtained through the `tecplot.sdk_version` attribute::

    >>> import tecplot
    >>> print(tecplot.sdk_version)
    16.3-0-74705
    >>> print(tecplot.sdk_version_info)
    SDKVersion(MajorVersion=16, MinorVersion=3, MajorRevision=0,
               MinorRevision=74705)
"""
from collections import namedtuple

from .tecutil import _tecinterprocess

Version = namedtuple('Version', ['major', 'minor', 'revision', 'build'])

version = '0.3.1'
build = '75100'
version_info = Version(*[int(x) for x in version.split('.')], build=build or 0)

sdk_version_info = _tecinterprocess.sdk_version_info
sdk_version = _tecinterprocess.sdk_version
