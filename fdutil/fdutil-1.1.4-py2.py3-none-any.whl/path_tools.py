
import os

__author__ = u'Oli Davis'
__copyright__ = u'Copyright (C) 2016 Oli Davis'


def expand_path(path):

    if path.startswith(u'./'):
        path = u'{p}{s}{f}'.format(p=os.getcwd(),
                                   s=os.sep,
                                   f=path[2:])

    if u'/' in path and u'/' != os.sep:
        path = path.replace(u'/', os.sep)

    return path


def ensure_path_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)
