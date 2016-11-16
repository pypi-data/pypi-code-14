import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def readme():
    try:
        with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as f:
            return f.read()
    except (IOError, OSError):
        return ''


def get_packages(package):
    """
    Return root package and all sub-packages.
    """
    return [dirpath
            for dirpath, dirnames, filenames in os.walk(package)
            if os.path.exists(os.path.join(dirpath, '__init__.py'))]


def get_package_data(package):
    """
    Return all files under the root package, that are not in a
    package themselves.
    """
    walk = [(dirpath.replace(package + os.sep, '', 1), filenames)
            for dirpath, dirnames, filenames in os.walk(package)
            if not os.path.exists(os.path.join(dirpath, '__init__.py'))]

    filepaths = []
    for base, filenames in walk:
        filepaths.extend([os.path.join(base, filename)
                          for filename in filenames])
    return {package: filepaths}


package = 'palmer'
install_requires = [
    'flask >= 0.10',
    'flask-swagger >= 0.2.13',
    'inflection >= 0.3.1',
    'msgpack-python >= 0.4.8',
    'speaklater >= 1.3'
]

setup(
    name='palmer',
    description="Redice Flask Boost Library. Inspired by flask-api.",
    long_description=readme(),
    version='0.0.4',
    packages=get_packages(package),
    package_data=get_package_data(package),
    install_requires=install_requires,
    license='MIT License',
    author='Redice',
    author_email='devteam@redice-inc.com',
    url='https://github.com/redice-inc/palmer',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython'
    ],
)
