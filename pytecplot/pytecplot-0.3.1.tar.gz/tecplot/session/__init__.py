"""|Tecplot Engine| and |Tecplot License| management.

The `session` module contains methods used to manipulate the |Tecplot Engine|
such as notification of a state-change that was done outside of PyTecplot.
It also contains methods for acquiring and releasing the |Tecplot License|.
"""

from .session import stop, acquire_license, release_license
from .state_changed import state_changed, zones_added
from .style import Style, get_style, set_style

import os
import platform
from ..tecutil import _tecinterprocess

def tecplot_install_directory():
    """|Tecplot 360 EX| installation directory.

    Top-level installation directory for |Tecplot 360 EX|. This will
    typically contain configuration files and the examples directory.
    """
    d = _tecinterprocess.tecsdkhome
    if platform.system() in ['Darwin','Mac']:
        d = os.path.normpath(os.path.join(d, '..', '..'))
    return d

def tecplot_examples_directory():
    """|Tecplot 360 EX| examples directory.

    Examples directory that is typically installed with |Tecplot 360 EX|.
    This may be overridden with the TECPLOT_EXAMPLES environment variable
    """
    d = tecplot_install_directory()
    return os.environ.get('TECPLOT_EXAMPLES', os.path.join(d, 'examples'))
