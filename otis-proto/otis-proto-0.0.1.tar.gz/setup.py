from setuptools import setup, find_packages

setup(
    name             = "otis-proto",
    description      = "Open Timeseries Interface Service protobuf bindings",
    url              = "https://github.com/hodgesds/otis-proto/python",
    version          = "0.0.1",
    author           = "Daniel Hodges",
    author_email     = "hodges.daniel.scott@gmail.com",
    scripts          = [],
    install_requires = [ "grpcio", "protobuf" ],
    test_suite       = "",
    tests_require    = [],
    packages         = find_packages(
        where        = '.',
        exclude      = ('tests*', 'bin*'),
    ),
)
