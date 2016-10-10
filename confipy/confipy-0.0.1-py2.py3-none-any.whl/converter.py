"""This module contains converter functions."""

import six
import confipy.notation

NOTATION_TYPES = {"dot": confipy.notation.DotNotation,
                  "dict": dict}


def _unflat_dict(flat_dict, unflat_dict=None, notation="dict"):
    """Convert flattened dict back to nested dict structure.

    Parameters
    ----------
    flat_dict: dict
        See _flatten_dict() for more information.
    unflat_dict: None, dict
        Parameter is used as parent dictionary.
    notation: {"dict", "dot"}, optional
        Provide notation type into which the unflattened dictionary will be
        converted to.

    Return
    ------
    unflattend_dict: dict

    """

    if not unflat_dict:
        notation_type = NOTATION_TYPES[notation]
        unflat_dict = notation_type()

    # iterate, begin with lowest depth
    sorted_items = sorted(flat_dict.items(), key=lambda x: len(x[0]))
    for key_chain, value in sorted_items:
        this_key = key_chain[0]
        # directly set value, if only one key is present
        if len(key_chain)== 1:
            unflat_dict[this_key] = value
            continue

        # check for existing key and account for DotNotation
        try:
            key_exists = unflat_dict[this_key]
        except (AttributeError, KeyError):
            key_exists = None

        # if key exists, do not create again
        if key_exists:
            _unflat_dict({key_chain[1:]: value}, key_exists, notation)
            continue

        unflat_dict[this_key] = _unflat_dict({key_chain[1:]: value},
                                             notation=notation)

    return unflat_dict


def _flat_dict(cfg_dict, parent=None, notation="dict"):
    """Convert nested dictionary into flattened dict of key-chain
    value pairs where the key-chain is a tuple of nested keys.

    For example, {"key1": {"key11":{"key111": "value1"}}}
    evaluates to  {("key1", "key11", "key111"): "value1"}.

    Simplifies dictionary operations for other parser functions.

    Parameters
    ----------
    cfg_dict: dict
        Dictionary containing config data.
    parent: None, optional
        For nested, recursive calls remembers the parent of current level.
    notation: {"dict", "dot"}, optional
        Provide notation type into which the unflattened dictionary will be
        converted by _unflat_dict later on. This information is required here
        because keys which are not strings cannot be used as attribute names
        for the DotNotation. Therefore, dictionaries containing non-string
        keys are not converted to DotNotation.

    Return
    ------
    flattened: dict

    """

    if not parent:
        parent = []

    # check for non string keys for dot notation
    if notation == "dot":
        if not all([isinstance(x, six.string_types) for x in cfg_dict.keys()]):
            return {tuple(parent):cfg_dict}

    flattened = {}
    for key, value in cfg_dict.items():
        key_level = parent + [key]

        # unflat nested dictionaries
        if isinstance(value, dict):
            flattened.update(_flat_dict(value, key_level, notation))
        else:
            key_chain = tuple(key_level)
            flattened[key_chain] = value

    return flattened