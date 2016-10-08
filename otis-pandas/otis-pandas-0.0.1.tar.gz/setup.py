from setuptools import setup, find_packages

setup(
    name             = "otis-pandas",
    description      = "Open Timeseries Interface Service pandas bindings",
    url              = "https://github.com/hodgesds/otis-pandas",
    version          = "0.0.1",
    author           = "Daniel Hodges",
    author_email     = "hodges.daniel.scott@gmail.com",
    scripts          = [],
    install_requires = [ "pandas", "otis", "otis-proto"],
    test_suite       = "",
    tests_require    = [ "tox", "nose" ],
    packages         = find_packages(
        where        = '.',
        exclude      = ('tests*', 'bin*', 'example*'),
    ),
)
