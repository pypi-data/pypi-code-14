"""This module contains the notation classes for the output configs."""


class DotNotation(object):
    """Enables dot notation for accessing config properties. This class does
    not inherit from dict on purpose in order to prevent namespace clashes.
    Therefore, only operator overloading methods are used which are unlikely
    to clash with variable names from config files.

    """

    def __getitem__(self, key):
        """Support bracketing attribute access. It is required to access
        attributes with builtin names like 'except'."""
        return getattr(self, key)

    def __setitem__(self, key, value):
        """Support bracketing attribute setting."""
        setattr(self, key, value)

    def __call__(self, ret="val", key=None, default=None):
        """Return specific attributes of the DotNotation instance.

        Parameters
        ----------
        ret: {"val", "dot", "dict", "get"}
            Define the return value. 'val' refers to attributes which are not
            DotNotation instances (therefore being str/lists by default).
            'dot' refers to attributes which are DotNotation instances. 'dict'
            provides the possibility to return itself as a dictionary. 'get'
            mimics the default dict.get() method. It returns the attribute if
            present. Otherwise returns the 'default' parameter.

        """

        if ret == "val":
            return {key: value for key, value in vars(self).items()
                    if not isinstance(value, DotNotation)}

        elif ret == "dot":
            return {key: value for key, value in vars(self).items()
                    if isinstance(value, DotNotation)}

        elif ret == "dict":
            res_dict = {}
            for key, value in vars(self).items():
                if isinstance(value, self.__class__):
                    res_dict[key] = value("dict")
                    continue
                res_dict[key] = value
            return res_dict

        elif ret == "get":
            if hasattr(self, key):
                return getattr(self, key)
            else:
                return default


    def __repr__(self):
        """Return string representation."""
        tpl = "CfgNode: {} nodes ({}) / {} values ({})"
        nodes = self("dot").keys()
        values = self("val").keys()
        return tpl.format(len(nodes), nodes, len(values), values)