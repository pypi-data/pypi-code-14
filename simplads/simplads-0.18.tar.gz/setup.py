from setuptools import setup

setup(
        name='simplads',
        version='0.18',
        author='Luke Avery',
        description=('A set of tools for conveniently using monads'),
        packages=[
            'simplads',
            'simplads.simplads',
            'simplads.simplads.namedtuples',
            'simplads.simplad_monad',
            'simplads.simplad_monad.namedtuples',
            'simplads.simplad_bundle'
        ]
)
