from setuptools import setup, find_packages
setup(
    name = "OLIVER",
    version = "0.13",
    packages = ['oliver'],
    test_suite = 'tests',

    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    install_requires = ['py4j','numpy','pandas'],

    #package_data = {
    #    # If any package contains *.txt or *.rst files, include them:
    #    '': ['*.txt', '*.rst'],
    #    # And include any *.msg files found in the 'hello' package, too:
    #    'hello': ['*.msg'],
    #},

    # metadata for upload to PyPI
    author = "Oliver Tessmer",
    author_email = "oliver.tessmer@gmail.com",
    description = "Convenience functions for interacting with the OLIVER workspace",
    #license = "PSF",
    keywords = "oliver",
    url = "https://msu.edu/~tessmero/",   # project home page, if any

    # could also include long_description, download_url, classifiers, etc.
)