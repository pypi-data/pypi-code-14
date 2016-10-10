"""This module contains the config reader."""

import yaml
import json
import collections

# python 2.7
try:
    import configparser
except ImportError:
    import ConfigParser as configparser


def _construct_unicode(self, node):
    """Override the default string handling function to always return unicode
    objects. Required for Python 2.7.

    Thanks to:

    http://stackoverflow.com/questions/2890146/how-to-force-pyyaml-to-load-strings-as-unicode-objects

    """
    return self.construct_scalar(node)


yaml.Loader.add_constructor(u'tag:yaml.org,2002:str', _construct_unicode)
yaml.SafeLoader.add_constructor(u'tag:yaml.org,2002:str', _construct_unicode)


def _read_configparser(fp):
    """Read configparser compliant config file from file like object.

    Parameters
    ----------
    fp: file-like object
        Any object having a read() method.

    Return
    ------
    cfg_dict: dict
        Dictionary containing config data.

    """

    cfg_parser = configparser.ConfigParser()

    # python 2.7
    try:
        cfg_parser.read_file(fp)
    except AttributeError:
        cfg_parser.readfp(fp)

    cfg_dict = {section: dict(cfg_parser.items(section))
                for section in cfg_parser.sections()}
    return cfg_dict


READER = collections.OrderedDict({"yaml": yaml.load,
                                  "configparser": _read_configparser,
                                  "json": json.load})

MIME_TYPES = {"yaml": READER["yaml"],
              "yml": READER["yaml"],
              "ini": READER["configparser"],
              "cfg": READER["configparser"],
              "json": READER["json"]}


def _read_infer(fp):
    """Iterates config reader functions and tries to find correct reader via
    try except statements.

    Parameters
    ----------
    fp: file-like object
        Any object having a read() method.

    Return
    ------
    cfg_dict: dict
        Dictionary containing config data.

    Raises
    ------
    IOError if no reader functions applies.

    """

    for read_label, read_func in READER.items():
        try:
            cfg_dict = read_func(fp)
        except Exception as error:
            print("Reader '{}' fails.".format(read_label))
        else:
            print("Reader '{}' succeeds.".format(read_label))
            return cfg_dict
        finally:
            fp.seek(0)
    else:
        raise IOError("Cannot find appropriate reader.")


def read_config(path_or_fp, read_engine="auto"):
    """Read config file and return as dictionary.

    Parameters
    ----------
    path_or_fp: str, file-like
        Path to config file to be read.
    read_engine: {"auto", "yaml", "json", "configparser"}
        Define the read engine to open the config file. By default, the file
        type is used to infer the correct read engine.

    Return
    ------
    cfg_dict: dict
        Key value pairs of config file.

    """

    # check for path or file-like object
    if hasattr(path_or_fp, "read"):
        fp = path_or_fp
        mime = read_engine
    else:
        fp = open(path_or_fp, "r")
        mime = path_or_fp.split(".")[-1].lower()

    read_function = MIME_TYPES.get(mime, _read_infer)
    cfg_dict = read_function(fp)

    return cfg_dict
