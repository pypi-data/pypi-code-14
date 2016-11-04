from setuptools import setup, find_packages

setup(
    name='pyxmacros',
    version='0.6',
    author='Andrew Leech',
    author_email='andrew@alelec.net',
    py_modules=['xmacros', 'pyxhook'],
    url='https://gitlab.alelec.net/corona/pyxmacros',
    license='BSD',
    install_requires=['python-xlib'],
#    dependency_links=['http://svn.code.sf.net/p/python-xlib/code/tags/xlib_0_15rc1/#egg=Xlib'],
#    dependency_links=['http://sourceforge.net/projects/python-xlib/files/python-xlib/0.15rc1/python-xlib-0.15rc1.tar.gz/download#egg=Xlib'],
    dependency_links=['http://sourceforge.net/projects/python-xlib/files/python-xlib/0.14/python-xlib-0.14.tar.gz/download#egg=Xlib'],
    description='A library to create macros on a linux system',
)


