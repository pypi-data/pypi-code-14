import fnmatch
import os
import json
from .utility import header


# this is more of a parse runner...
class JupyterParser(object):
    """
    parser class that defines hooks for plugins
    to parse jupyter notebook
    """

    def __init__(self, root, plugins):
        """initialize parser instance

        Arguments
        ---------
        root : string
            root directory for finding ipython notebook files

        plugins : [array-like] of plugins instances
            plugin instances must support the following methods or pass
            - parse_notebook : passes notebook to plugin
            - summary : summary statistics of plugin presented
        """
        self.root = root
        self.extension = 'ipynb'
        self.plugins = plugins

    def parse(self):
        """after initialization, parse noteobooks"""
        # get all the files in root directory and subdirectories
        filenames_ = []
        for root, dirnames, filenames in os.walk(self.root):
            for filename in fnmatch.filter(filenames, '*.%s' % (self.extension)):
                # could just move logic here?
                filenames_.append(os.path.join(root, filename))

        for filename in filenames_:
            # open up each of the files
            try:
                notebook = json.load(open(filename))
            except ValueError:
                # this file wasn't actually a notebook
                continue
            for plugin in self.plugins:
                plugin.parse_notebook(filename, notebook)

        for plugin in self.plugins:
            plugin_name = plugin.__class__.__name__
            print(header(plugin_name))
            plugin.summary()
