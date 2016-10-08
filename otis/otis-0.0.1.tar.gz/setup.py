from setuptools import setup, find_packages

setup(
    name             = "otis",
    description      = "Open Timeseries Interface Service",
    url              = "https://github.com/hodgesds/otis-python",
    version          = "0.0.1",
    author           = "Daniel Hodges",
    author_email     = "hodges.daniel.scott@gmail.com",
    scripts          = [ "bin/otis" ],
    install_requires = [ "otis-proto", "grpcio" ],
    test_suite       = "",
    tests_require    = [ "tox", "nose" ],
    packages         = find_packages(
        where        = '.',
        exclude      = ('tests*', 'bin*'),
    ),
)
