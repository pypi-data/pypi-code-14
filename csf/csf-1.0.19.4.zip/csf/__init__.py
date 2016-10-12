# coding=utf8
import sys

if sys.version < "3":
    stdout = sys.stdout
    stderr = sys.stderr
    stdin = sys.stdin
    reload(sys)
    sys.stdout = stdout
    sys.stderr = stderr
    sys.stdin = stdin
    sys.setdefaultencoding("utf-8")



from .conf import config
from .api import *

__version__ = "1.0.19.4"
config.version = __version__