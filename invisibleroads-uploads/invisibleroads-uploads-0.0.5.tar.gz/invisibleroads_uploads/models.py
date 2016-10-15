from glob import glob
from invisibleroads_macros.disk import remove_safely
from os.path import join


class Upload(object):

    def __init__(self, folder):
        self.folder = folder
        try:
            self.path = glob(join(folder, 'raw*'))[0]
        except IndexError:
            raise IOError
        self.name = open(join(folder, 'name.txt')).read()
