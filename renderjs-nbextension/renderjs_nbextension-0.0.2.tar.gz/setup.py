# -*- coding: utf-8 -*-
from setuptools import setup

try:
    from jupyterpip import cmdclass
except:
    print("!!!! NO JUPYTER PIP !!!!")

setup(
    name='renderjs_nbextension',
    version='0.0.2',
    packages=['renderjs_nbextension'],
    install_requires=['jupyter-pip'],
    cmdclass=cmdclass('renderjs_nbextension', 'renderjs_nbextension/main'
                      # Flag for user install
                      #,True
    ),

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
