from os import path
import logging

from ..tecutil import _tecutil, lock
from .. import constant, session
from ..exception import TecplotSystemError

log = logging.getLogger(__name__)

__all__ = ['export_image']

@lock()
def export_image(filename, image_type=None):
    """Exports image to file.

    Parameters:
        filename (`string <str>`): File name with a valid extension (unless
            *image_type* is specified).
        image_type (`string <str>`, optional): Type of image to be
            generated. (default: `None`)

    Supported image types:
        * `png <https://en.wikipedia.org/wiki/Portable_Network_Graphics>`_

    .. code-block:: python
        :emphasize-lines: 3

        >>> import tecplot
        >>> tecplot.load_layout('mylayout.lay')
        >>> tecplot.export_image('image.png')
    """
    export_by_extension = {'png' : png}
    extension = (image_type or path.splitext(filename)[-1][1:]).lower()
    export_by_extension[extension](filename)

@lock()
def png(filename):
    _tecutil.ExportSetup('EXPORTFNAME', None, 0, filename)
    _tecutil.ExportSetup('EXPORTFORMAT', None, 0, constant.ExportFormat.PNG)
    if not _tecutil.Export(False):
        raise TecplotSystemError('could not export image: {}'.format(filename))
    log.info('image file created: '+filename)
