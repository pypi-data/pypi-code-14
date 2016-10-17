
import os
import logging
import umodules.helper as helper

from umodules.module_type import IModuleType
from urllib.parse import urlparse


def _run(project, module):
    """Pull a Module from a Local Source.

    Local Modules are 'usually' relative to the Main Project

    :param project:
    :param module:
    """
    src = os.path.abspath(urlparse('{0}/{1}'.format(module.url, module.name)).path)
    dst = os.path.abspath('{0}/{1}/Assets/{2}'.format(project.repository_path, module.name, module.name))

    logging.debug('- checking for {0}'.format(src))
    if (os.path.exists(src)):
        logging.debug('- copying to repo at {0}'.format(dst))
        helper.copy_tree(src, dst)
    else:
        raise Exception('Local Module {0} was Not Found'.format(module.name))


class LocalCopy(IModuleType):

    def __init__(self):
        super().__init__()
        self.name = 'local_copy'

    def install(self, project):
        return super().install(project)

    def pull(self, project, module):
        _run(project, module)

