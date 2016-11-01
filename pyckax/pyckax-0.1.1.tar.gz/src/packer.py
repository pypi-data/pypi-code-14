'''
pyckax.packer
'''
import re, os, setuptools

class Packer:
    '''
    '''
    # +-------------------------------------------------------------------------
    def __init__(self, **info):
        self.info = info
    # +-------------------------------------------------------------------------
    def setup(self, **info):
        self.info.update(info)
        setuptools.setup(**self.info)
    # +-------------------------------------------------------------------------
    def loadVersion(self, path, coding='utf-8'):
        pattern = re.compile(r'__version__\s*=\s*\'((\d|\.)+)\'')
        with open(os.path.abspath(path), 'rb') as f:
            text = f.read().decode(coding)
            match = pattern.search(text);
            if match: self.info['version'] = match.group(1)
    # +-------------------------------------------------------------------------
    def loadLongDescription(self, path, coding='utf-8'):
        with open(os.path.abspath(path), 'rb') as f:
            text = f.read().decode(coding)
            self.info['long_description'] = text
    # +-------------------------------------------------------------------------
    def pickPackage(self, root, directory):
        result = [ root ]
        folder = { root: directory }
        for other in setuptools.find_packages(directory):
            name = root + '.' + other
            result.append(name)
            folder[name] = directory + '/' + other.replace('.', '/')
        if 'packages' in self.info:
            self.info['packages'].extend(result)
        else: self.info['packages'] = result
        if 'package_dir' in self.info:
            self.info['package_dir'].update(folder)
        else: self.info['package_dir'] = folder
