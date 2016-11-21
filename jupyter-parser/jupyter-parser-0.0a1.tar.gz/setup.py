from setuptools import setup, find_packages

setup(
    name='jupyter-parser',
    version='0.0a1',
    description='a command line tool for parsing jupyter notebooks',
    url='https://github.com/cameres/jupyter-parser',
    author='Connor Ameres',
    author_email='connorameres@gmail.com',
    license='Mozilla Public License 2.0 (MPL 2.0)',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
        'Topic :: Software Development',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5'
    ],
    keywords='jupyter notebook parser plugins',
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    install_requires=[
        'click',
    ],
    entry_points='''
        [console_scripts]
        jupyter-parser=jupyter_parser:parse
    '''
)
