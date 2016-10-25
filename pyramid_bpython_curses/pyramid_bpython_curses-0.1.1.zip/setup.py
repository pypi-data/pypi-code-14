from setuptools import setup
import os

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()

requires = [
    'bpython',
    'pyramid > 1.6a2',
]

entry_points = {
    'pyramid.pshell_runner': [
        'bpython_curses = pyramid_bpython_curses:bpython_curses_shell_runner',
    ],
}

setup(
    name='pyramid_bpython_curses',
    version='0.1.1',
    description='pyramid bpython curses pshell',
    long_description=README,
    author='Iivari Mokelainen',
    author_email='iivmok@gmail.com',
    url='https://github.com/iivmok/pyramid_bpython_curses',
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Framework :: Pyramid",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI",
    ],
    license="LICENSE.txt",
    zip_safe=False,
    py_modules=['pyramid_bpython_curses'],
    install_requires=requires,
    entry_points=entry_points,
)
