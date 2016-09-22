#
import os
import re
import warnings
import ConfigParser
import StringIO
import logging

try:
    os.path.expanduser('~')
    expanduser = os.path.expanduser
except (AttributeError, ImportError):
    # This is probably running on App Engine.
    expanduser = (lambda x: x)
try:
    import simplejson as json
except ImportError:
    import json

# By default we use two locations for the footmark logging configurations,
# /etc/footmark/logging.ini and ~/.footmark/logging.ini (which works on Windows and Unix).
FootmarkConfigPath = '/etc/footmark/logging.ini'
FootmarkConfigLocations = [FootmarkConfigPath]
UserConfigPath = os.path.join(expanduser('~'), '.footmark')
FootmarkConfigLocations.append(UserConfigPath)

# If there's a FOOTMARK_CONFIG variable set, we load ONLY
# that variable
if 'FOOTMARK_CONFIG' in os.environ:
    FootmarkConfigLocations = [expanduser(os.environ['FOOTMARK_CONFIG'])]

# If there's a FOOTMARK_PATH variable set, we use anything there
# as the current configuration locations, split with os.pathsep.
elif 'FOOTMARK_PATH' in os.environ:
    FootmarkConfigLocations = []
    for path in os.environ['FOOTMARK_PATH'].split(os.pathsep):
        FootmarkConfigLocations.append(expanduser(path))

# Default logging configurations.
# By default we use location /var/footmark/ for the footmark logs.
LoggingDict = '/Users/xiaozhu/hehehe/footmark/logs/'
LoggingDictConfig = {
    'version':1,
    'formatters': {
        'default': {
            'format': '%(asctime)s [%(levelname)s] %(filename)s %(funcName)s %(lineno)d: %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
            'level': 'DEBUG',
            'stream': 'ext://sys.stdout'
        },
        'file': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'formatter': 'default',
            'level': 'DEBUG',
            'filename': LoggingDict+'footmark.log',
            'when': 'M',
            'interval': 1,
            'backupCount': 7
        }
    },
    "loggers": {
        'footmark': {
            'level': 'DEBUG',
            'handlers': ['console', 'file']
        }
    }
}