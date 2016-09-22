import os
import logging
from io import StringIO
from collections import defaultdict
from pprint import pformat
from configparser import ConfigParser
from funmap import funmap

logger = logging.getLogger(__name__)

MAIN = 'dummy main section'

def Defaults(config_file, config_sep):
    '''
    :param str config_file: Configuration file
    :type config_sep: str or NoneType
    ;param config_sep: Character to separate sections, or None to indicate no sectioning
    :rtype: dict
    :returns: Stuff from the config file
    '''
    d = _rdict()

    if config_file and os.path.isfile(config_file):
        if config_sep:
            fp = open(config_file)
        else:
            fp = StringIO()
            fp.write('[%s]\n' % MAIN)
            with open(config_file) as gp:
                fp.write(gp.read())
            fp.seek(0)

        c = ConfigParser()
        c.read_file(fp)

        if config_sep:
            for config_section in c.sections():
                y = d
                if config_sep:
                    for component in config_section.split(config_sep):
                        y = y[component]
                y.update(c[config_section])

                w = (config_file, config_section, pformat(y))
                logger.info('Defaults from %s,\n  section [%s]:\n%s' % w)

            d = _as_dict(d)
        else:
            d = c[MAIN]

    else:
        d = {}
    return d

def _rdict():
    return defaultdict(_rdict)

def _as_dict(x):
    if isinstance(x, defaultdict):
        return {k: _as_dict(v) for k, v in x.items()}
    else:
        return x
