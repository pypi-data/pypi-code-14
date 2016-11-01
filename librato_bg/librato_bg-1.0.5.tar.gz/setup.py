from setuptools import setup

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst', 'md')
except ImportError:
    print("Warning: pypandoc module not found, could not convert Markdown to RST")
    long_description = open('README.md', 'r').read()


def _is_requirement(line):
    """Returns whether the line is a valid package requirement."""
    line = line.strip()
    return line and not (line.startswith("-r") or line.startswith("#"))


def _read_requirements(filename):
    """Returns a list of package requirements read from the file."""
    requirements_file = open(filename).read()
    return [line.strip() for line in requirements_file.splitlines()
            if _is_requirement(line)]


base_packages = _read_requirements("requirements/base.txt")
test_packages = _read_requirements("requirements/tests.txt")


# from https://gist.github.com/techtonik/4066623
# This is necessary, because librato is indirectly imported in
# librate_bg/__init__.py. But setup.py must be runnable without having the
# dependencies installed.
def get_version(relpath):
    """Read version info from a file without importing it"""
    from os.path import dirname, join

    if '__file__' not in globals():
        # Allow to use function interactively
        root = '.'
    else:
        root = dirname(__file__)

    # The code below reads text file with unknown encoding in
    # in Python2/3 compatible way. Reading this text file
    # without specifying encoding will fail in Python 3 on some
    # systems (see http://goo.gl/5XmOH). Specifying encoding as
    # open() parameter is incompatible with Python 2

    # cp437 is the encoding without missing points, safe against:
    #   UnicodeDecodeError: 'charmap' codec can't decode byte...

    for line in open(join(root, relpath), 'rb'):
        line = line.decode('cp437')
        if '__version__' in line:
            if '"' in line:
                # __version__ = "0.9"
                return line.split('"')[1]
            elif "'" in line:
                return line.split("'")[1]


setup(
    name='librato_bg',
    version=get_version('librato_bg/__init__.py'),
    description="Enables submitting of Librato events in a background thread",
    long_description=long_description,

    url='https://github.com/nyaruka/python-librato-bg',
    license='MIT License',

    author='Nyaruka',
    author_email='code@nyaruka.com',

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],

    packages=['librato_bg'],
    install_requires=base_packages,
    tests_require=base_packages + test_packages,
)
