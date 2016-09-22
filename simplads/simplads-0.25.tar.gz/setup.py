from setuptools import setup

setup(
        name='simplads',
        version='0.25',
        author='Luke Avery',
        author_email='cogmob@gmail.com',
        url='https://github.com/Cogmob/simplads',
        description=('A set of tools for conveniently using monads'),
        packages=[
            'simplads',
            'simplads.simplads',
            'simplads.simplads.namedtuples',
            'simplads.simplad_monad',
            'simplads.simplad_monad.namedtuples',
            'simplads.simplad_bundle'
        ],
        long_description=open('README.rst', 'r').read()
)
