from setuptools import setup, find_packages

setup(
    name = 'DeFCoM',
    version = "1.0.0",
    packages = ['defcom'],
    #scripts = ['.py'],

    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    install_requires = ['docutils>=0.3', 'pysam>=0.9', 'scikit-learn>=0.16', 
        'numpy>=1.8', 'scipy>=0.14'],

    #Provide websites with source for required dependencies
    dependency_links = [
        "git+https://github.com/pysam-developers/pysam",
        "https://sourceforge.net/projects/numpy/",
        "git+https://github.com/scipy/scipy/releases",
        "git+https://github.com/scikit-learn/scikit-learn/releases"
    ],

    #Required version of python
    #python_requires = 'python>=2.7.0',

    package_data = {
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt', '*.rst'],
        # And include any *.msg files found in the 'hello' package, too:
        'hello': ['*.msg'],
    },

    # metadata for upload to PyPI
    author = "Bryan Quach",
    author_email = "bryancquach@gmail.com",
    description = "A supervised learning genomic footprinter",
    license = "PSF",
    keywords = "defcom genomics footprinter footprinting",
    url = "https://bitbucket.org/bryancquach/defcom",   # project home page

    # could also include long_description, download_url, classifiers, etc.
)
