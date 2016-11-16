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

install_requires = [
    'enum34 >= 1.1.6',
    'inflection >= 0.3.1',
    'Pillow >= 3.3.1',
    'python-magic >= 0.4.12',
    'six >= 1.10.0',
    'SQLAlchemy >= 1.0.15',
    'SQLAlchemy-Enum34 >= 1.0.1',
    'SQLAlchemy-Utils >= 0.32.9',
    'SQLAlchemy-Wrapper >= 1.7.0'
]

setup(
    name='palvin',
    description="Redice SQLAlchemy Boost Library. It's based sqlalchemy-wrapper",
    long_description=readme(),
    version='0.0.2',
    packages=['palvin'],
    package_dir={'palvin': 'palvin'},
    package_data={},
    install_requires=install_requires,
    license='MIT License',
    author='Redice',
    author_email='devteam@redice-inc.com',
    url='https://github.com/redice-inc/palvin',
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
