"""The scaffholder command."""


from json import dumps
import codedeploy_generator

from .base import Base


class Create(Base):
    """Say hello, world!"""

    def run(self):
        import os
        from distutils.dir_util import copy_tree

        path = os.path.abspath(codedeploy_generator.__file__)
        dir_path = os.path.dirname(path)
        directory = os.getcwd()+'/src'

        if not os.path.exists(directory):
            os.makedirs(directory)

        copy_tree(dir_path+'/extra/', os.getcwd())