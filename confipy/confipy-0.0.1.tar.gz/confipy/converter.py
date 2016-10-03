"""This module contains converter functions."""

class DotNotation(object):
    """Enables dot notation for accessing config properties."""

    def get(self, key, default=None):
        if hasattr(self, key):
            return getattr(self, key)
        return default

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __repr__(self):
        tpl = "CfgNode: {} nodes ({}) / {} values ({})"
        nodes = [x for x in vars(self)
                 if isinstance(getattr(self,x), DotNotation)]
        values = [x for x in vars(self)
                  if not isinstance(getattr(self,x), DotNotation)]
        return tpl.format(len(nodes), nodes, len(values), values)


def _unflat_dict(flat_dict, unflat_dict=None, default_type=dict):
    """Convert flattened dict back to nested dict structure.

    Parameters
    ----------
    flat_dict: dict
        See _flatten_dict() for more information.
    unflat_dict: None, dict
        Parameter is used as parent dictionary.

    Return
    ------
    unflattend_dict: dict

    """

    if not unflat_dict:
        unflat_dict = default_type()

    # iterate, begin with lowest depth
    sorted_items = sorted(flat_dict.items(), key=lambda x: len(x[0]))
    for key_chain, value in sorted_items:
        this_key = key_chain[0]
        # directly set value, if only one key is present
        if len(key_chain)== 1:
            unflat_dict[this_key] = value
            continue

        # if key exists, do not create again
        key_exists = unflat_dict.get(this_key)
        if key_exists:
            _unflat_dict({key_chain[1:]: value}, key_exists, default_type)
            continue

        unflat_dict[this_key] = _unflat_dict({key_chain[1:]: value},
                                             default_type=default_type)

    return unflat_dict


def _flat_dict(cfg_dict, parent=None):
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

    Return
    ------
    flattened: dict

    """

    if not parent:
        parent = []

    flattened = {}
    for key, value in cfg_dict.items():
        key_level = parent + [key]
        if isinstance(value, dict):
            flattened.update(_flat_dict(value, key_level))
        else:
            key_chain = tuple(key_level)
            flattened[key_chain] = value

    return flattened