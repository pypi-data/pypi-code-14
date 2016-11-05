import logging
from io import StringIO
from pprint import pformat
from collections import defaultdict
from configparser import ConfigParser
from .signature import Signature

logger = logging.getLogger(__name__)

MAIN = 'dummy main section'

def write(prog, config_fp, config_sep):
    '''
    :param Program prog: Function, nested functions, &c.
    :type config_fp: File-like object with text write flags
    :param config_fp: Configuration file
    :type config_sep: str or NoneType
    :param config_sep: Character to separate sections, or None to indicate no sectioning
    '''
    if config_sep:
        d = _rdict()
        for section in prog:
            str_section = config_sep.join(section)
            d[str_section] = {}
            for key, param in Signature(prog[section]).keyword2.items():
                d[str_section][key] = param
    else:
        d = {}
        for section in prog:
            for key, param in Signature(prog[section]).keyword2.items():
                if key in d:
                    if param.default != d[key]:
                        msg = 'There are different defaults for -%s. Make the defaults match, use different names, or set a config_sep.'

                        raise ValueError(msg % key)
                else:
                    d[key] = param
        d = {MAIN: d}
    
    c = ConfigParser()
    for section, contents in sorted(d.items()):
        c.add_section(section)
        for k in sorted(contents):
            param = contents[k]
            try:
                if param.call(repr(param.default)) == param.default:
                    c[section][k] = repr(param.default)
            except Exception:
                pass

    with StringIO() as gp:
        c.write(gp)
        gp.seek(0)
        if not config_sep:
            gp.readline()
        config_fp.write(gp.read())

def read(config_fp, config_sep):
    '''
    :type config_fp: File-like object with text read flags
    :param config_fp: Configuration file
    :type config_sep: str or NoneType
    :param config_sep: Character to separate sections, or None to indicate no sectioning
    :rtype: dict
    :returns: Stuff from the config file
    '''
    d = _rdict()

    if config_fp:
        if config_sep:
            fp = config_fp
        else:
            fp = StringIO()
            fp.write('[%s]\n' % MAIN)
            fp.write(config_fp.read())
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

                w = (config_section, pformat(y))
                logger.info('Defaults from section [%s]:\n%s' % w)

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
