"""Module to make it easier to work with lots of parameters."""

import yaml

__version__ = "0.1.0"


class Parameters(dict):
    """Class for storing, reading in and writing out parameters."""

    @classmethod
    def from_yaml(cls, string):
        """Return Parameter instance from yaml string."""
        p = cls()
        d = yaml.load(string)
        if not isinstance(d, dict):
            raise(TypeError("YAML is not a dictionary at the top level"))
        p.update(d)
        return p

    @classmethod
    def from_file(cls, fpath):
        """Read parameters from file."""
        with open(fpath, "r") as fh:
            return cls.from_yaml(fh.read())

    def to_yaml(self):
        """Return yaml string representation."""
        return yaml.dump(dict(self),
                         explicit_start=True,
                         default_flow_style=False)

    def to_file(self, fpath):
        """Write parameters to file."""
        with open(fpath, "w") as fh:
            fh.write(self.to_yaml())
