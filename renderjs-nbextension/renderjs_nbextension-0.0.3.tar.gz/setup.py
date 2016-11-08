# -*- coding: utf-8 -*-
from setuptools import setup
from setuptools.command.install import install

class Install_nbextension(install):

    def run(self):
        print("## In install_nbextension")
        print("##")

        try:
            from notebook.nbextensions import install_nbextension
            from notebook.services.config import ConfigManager
            print("## Success")
        except:
            print("## Could not import notebook.*")

setup(
    name='renderjs_nbextension',
    version='0.0.3',
    packages=['renderjs_nbextension'],
    cmdclass = {
        'install': Install_nbextension,
    },

    package_data = {
        '': ['*.js', '*.html']
    },

    # PyPI Data
    author='Sebastian Kreisel',
    author_email='sebastian.kreisel@nexedi.com',
    description='RenderJS gadgets for jupyter (frontend-part)',
    keywords='renderjs jupyter nbextension',
    license='GPL 2',
    url='https://lab.nexedi.com/Kreisel/renderjs_extension'
)
