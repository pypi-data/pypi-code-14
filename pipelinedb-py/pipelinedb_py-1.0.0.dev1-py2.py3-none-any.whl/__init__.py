__author__ = 'Shihui He'
__versioninfo__ = (1, 0, 0)
__version__ = '.'.join(map(str, __versioninfo__))
__title__ = 'pipelinedb-py'

from .client import PipelineDBClient
from .errors import PipelineDBUnfoundError
