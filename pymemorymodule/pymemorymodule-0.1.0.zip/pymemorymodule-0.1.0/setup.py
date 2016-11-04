from distutils.cmd import Command

try:
    from setuptools import setup, Extension
except ImportError:
    from distutils.core import setup, Extension

import os
import sys
import textwrap
import warnings
import subprocess

here = os.path.abspath(os.path.dirname(__file__))


def from_here(*paths):
    global here
    return os.path.join(here, *paths)


def safe_splitlines(text):
    return textwrap.dedent(text).strip().splitlines()


def get_long_description():
    try:
        with open(from_here("README.rst")) as fp:
            return fp.read()
    except IOError:
        warnings.warn("README.rst was not found", stacklevel=2)
        return ""


class BaseCommand(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run_and_exit(self, *args, **kwargs):
        global here
        kwargs["cwd"] = here
        raise SystemExit(
            subprocess.call(*args, **kwargs)
        )


class TestCommand(BaseCommand):
    description = "Run tests."

    def run(self):
        popenargs = (
            [sys.executable, "-m", "test"],
        )
        self.run_and_exit(*popenargs)


class Md2RstCommand(BaseCommand):
    description = "Convert README.md to README.rst."

    def run(self):
        global here
        pyscript = """\
            from os.path import join
            from pypandoc import convert, get_pandoc_path
            from pypandoc.pandoc_download import download_pandoc
            exec('try: path = get_pandoc_path()\\nexcept: path = None')
            path or download_pandoc()
            source = join(r'{HERE}', 'README.md')
            target = join(r'{HERE}', 'README.rst')
            convert(source, 'rst', 'md', outputfile=target)
        """.format(HERE=here)
        pyoneliner = ";".join(safe_splitlines(pyscript))
        popenargs = (
            [sys.executable, "-c", pyoneliner],
        )
        self.run_and_exit(*popenargs)


classifiers = """\
License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)
Development Status :: 3 - Alpha
Environment :: Win32 (MS Windows)
Programming Language :: C
Programming Language :: Python :: 2.6
Programming Language :: Python :: 2.7
Programming Language :: Python :: 3.3
Programming Language :: Python :: 3.4
Programming Language :: Python :: 3.5
Operating System :: Microsoft :: Windows
Intended Audience :: Developers
"""

keywords = """\
MemoryModule
DLL
Windows
"""

pymemorymodule = Extension(
    "pymemorymodule",
    sources=[from_here("pymemorymodule.c"), from_here("MemoryModule.c")],
    depends=[from_here("MemoryModule.h")],
)

setup(
    version='0.1.0',
    name="pymemorymodule",
    license="MPL2.0",
    url="https://bitbucket.org/sakurai_youhei/pymemorymodule/overview",
    description="PyMemoryModule is a Python binding for MemoryModule.",
    long_description=get_long_description(),
    classifiers=safe_splitlines(classifiers),
    keywords=safe_splitlines(keywords),
    author="Youhei Sakurai",
    author_email="sakurai.youhei@gmail.com",
    ext_modules=[pymemorymodule],
    cmdclass={
        "test": TestCommand,
        "md2rst": Md2RstCommand,
    },
)
