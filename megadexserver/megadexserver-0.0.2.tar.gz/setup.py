from setuptools import setup, find_packages

setup(
    name             = "megadexserver",
    description      = "Mega Indexer Server",
    url              = "https://github.com/hodgesds/megadex-server",
    version          = "0.0.2",
    author           = "Daniel Hodges",
    author_email     = "hodges.daniel.scott@gmail.com",
    include_package_data = True,
    scripts          = [ "bin/megadex-server" ],
    install_requires = [
                        "elasticsearch",
                        "gevent",
                        "flask",
                       ],
    test_suite       = "",
    tests_require    = [ "tox", "nose" ],
    package_data     = { 'megadexserver': ['static/*', 'templates/*'], },
    packages         = find_packages(
        where        = ".",
        exclude      = ("tests*", "bin*", "example*"),
    ),
)
