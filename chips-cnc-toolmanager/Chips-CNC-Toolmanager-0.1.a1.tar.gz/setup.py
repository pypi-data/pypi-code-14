import codecs
import os
import re

from setuptools import setup, find_packages

#setup.py based on https://hynek.me/articles/sharing-your-labor-of-love-pypi-quick-and-dirty/

###################################################################

NAME = "Chips-CNC-Toolmanager"
PACKAGES = find_packages()
META_PATH = os.path.join("chips", "__init__.py")
KEYWORDS = ["machining", "CNC", "tools","CAM", "g-code","workshop"]
CLASSIFIERS = [
#https://pypi.python.org/pypi?%3Aaction=list_classifiers
    "Development Status :: 3 - Alpha",
    "Intended Audience :: End Users/Desktop",
    "Natural Language :: English",
    "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    "Operating System :: OS Independent",
    "Environment :: X11 Applications",
    "Environment :: X11 Applications :: Qt",
    "Environment :: Win32 (MS Windows)",
    "Environment :: MacOS X",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 2.6",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: Implementation :: CPython",
    "Programming Language :: Python :: Implementation :: PyPy",
    "Topic :: Other/Nonlisted Topic",
]
INSTALL_REQUIRES = ["camelot==13.04.13-gpl-pyqt"]

###################################################################

HERE = os.path.abspath(os.path.dirname(__file__))

def read(*parts):
    """
    Build an absolute path from *parts* and and return the contents of the
    resulting file.  Assume UTF-8 encoding.
    """
    with codecs.open(os.path.join(HERE, *parts), "rb", "utf-8") as f:
        return f.read()


META_FILE = read(META_PATH)


def find_meta(meta):
    """
    Extract __*meta*__ from META_FILE.
    """
    meta_match = re.search(
        r"^__{meta}__ = ['\"]([^'\"]*)['\"]".format(meta=meta),
        META_FILE, re.M
    )
    if meta_match:
        return meta_match.group(1)
    raise RuntimeError("Unable to find __{meta}__ string.".format(meta=meta))


if __name__ == "__main__":
    setup(
        name=NAME,
        description=find_meta("description"),
        license=find_meta("license"),
        url=find_meta("uri"),
        version=find_meta("version"),
        author=find_meta("author"),
        author_email=find_meta("email"),
        maintainer=find_meta("author"),
        maintainer_email=find_meta("email"),
        keywords=KEYWORDS,
        long_description=read("README"),
        py_modules = ['Chips'],
        packages=PACKAGES,
        package_dir={"": "./"},

        # If there are data files included in your packages that need to be
        # installed, specify them here.  If using Python 2.6 or less, then these
        # have to be included in MANIFEST.in as well.
        package_data={'chips': ['art/chips_iconset/128x128/*.png', '*.png' ],'chips': ['default_gcodes/*.nc'],},
        include_package_data=True,
        zip_safe=False,
        entry_points = {'gui_scripts':['Chips = Chips:start_application',],},
        classifiers=CLASSIFIERS,
        install_requires=INSTALL_REQUIRES,
    )

