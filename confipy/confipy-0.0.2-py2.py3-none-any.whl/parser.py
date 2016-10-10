"""This module contains the config parser functions."""

import os
import six
import confipy.reader
import confipy.converter

ERR_CFG_NOT_FOUND = "Cannot find referenced config '{}'."


def parsing_handler(parsers, flattened_dict, **kwargs):
    """Delegates positional and keyword arguments to parser functions.
    Returns parsed config as flattened dictionary.

    Parameters
    ----------
    parsers: iterable
        Parser names which are executed sequentially.
    flattened_dict: dict
        Config data as flattened dictionary.

    Return
    ------
    parsed_cfg: dict
        Flattened dictionary.

    """

    parsers_opt = {"include": include,
                   "substitute": substitute}

    for parser in parsers:
        parsed_cfg = parsers_opt[parser](flattened_dict, **kwargs)

    return parsed_cfg


def include(flattened_dict, source_path=None, marker="$include", **kwargs):
    """Scan config dictionary for include statements. Load and insert
    referenced config files under corresponding key's namespace.

    Parameters
    ----------
    flattened_dict: dict
        Flattened dictionary containing config data.
    source_path: str
        Path to original config file. Necessary for relative includes.
    marker: str, optional
        Set keyword to define include values.

    Return
    ------
    parsed_dict: dict

    """

    cwd = os.path.dirname(source_path)
    parsed_dict = {}

    for key_chain, value in flattened_dict.items():
        try:
            if not value.startswith(marker):
                parsed_dict[key_chain] = value
                continue
        except AttributeError:
            parsed_dict[key_chain] = value
            continue

        absolute_path = value.replace(marker, "").lstrip().rstrip()
        relative_path = os.path.join(cwd, absolute_path)

        # check relative path first, if not found, absolute path second
        if os.path.exists(relative_path):
            path = relative_path
        elif os.path.exists(absolute_path):
            path = absolute_path
        else:
            raise AssertionError(ERR_CFG_NOT_FOUND.format(absolute_path))

        # load, flatten and include referenced config under its own namespace
        inc_cfg = confipy.reader.read_config(path)
        inc_flat = confipy.converter._flat_dict(inc_cfg, list(key_chain))
        inc_included = include(inc_flat, path)
        parsed_dict.update(inc_included)

    return parsed_dict


def substitute(to_parse, parsed=None, splitter=" + ", marker="$", **kwargs):
    """Find keys identified by splitter and marker signs. Only values
    containing the splitter are taken into account. Splitted values must have
    keys which begin with the marker sign. Otherwise, keys are ignored.

    The function calls itself recursively until to_parse is empty.

    Parameters
    ----------
    to_parse: dict
        Dictionary with items to be parsed.
    parsed: dict
        Dictionary with valid lookup items for substitution usage.
    splitter: str
        The splitter to identify possible keys.
    marker: str
        The marker to identify correct keys.

    Return
    ------
    parsed: dict

    """

    # return result if to_parse is empty
    if not to_parse:
        return parsed

    # if there's nothing yet, find all non-subs items
    if not parsed:
        parsed = {key: value for key, value in to_parse.items()
                  if not _contains(value, splitter)}
        to_parse = {key: value for key, value in to_parse.items()
                    if key in set(parsed) ^ set(to_parse)}

    # iterate items to be parsed; distinguish strings and lists
    for key, value in to_parse.copy().items():
        if isinstance(value, six.string_types):
            valid = _substitue_value(value, parsed, splitter, marker)
        else:
            valid = [_substitue_value(element, parsed, splitter, marker)
                     if _contains(element, splitter) else element
                     for element in value]

        if all(valid):
            del to_parse[key]
            parsed[key] = valid

    return substitute(to_parse, parsed)


def _substitue_value(value, parsed, splitter, marker):
    """Substitute keys of a singular string. Returns False if one key could
    not successfully be replaced.

    Parameters
    ----------
    value: str
        String value containing keys to be substituted.
    parsed: dict
        Dictionary with valid lookup items for substitution usage.
    splitter: str
        The splitter to identify possible keys.
    marker: str
        The marker to identify correct keys.

    Return
    ------
    parsed_item: str, None

    """

    parsed_item = ""
    for part in value.split(splitter):
        if not part.startswith(marker):
            parsed_item += part
            continue

        key_chain = _convert_key_chain(part[1:])
        parsed_value = parsed.get(key_chain)

        if not parsed_value:
            return [False]

        parsed_item += parsed_value

    return parsed_item


def _contains(values, splitter):
    """Check presence of marker in values.

    Parameters
    ----------
    values: str, iterable
        Either a single value or a list of values.
    splitter: str
        The target to be searched for.

    Return
    ------
    boolean

    """

    if isinstance(values, six.string_types):
        values = (values,)

    try:
        if any([splitter in x for x in values]):
            return True
        return False
    except TypeError:
        return False


def _convert_key_chain(key_string):
    """Convert dot notation to tupled key chain notation"""

    return tuple(key_string.split("."))
