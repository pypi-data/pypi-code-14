from setuptools import setup

if __name__ == '__main__':
    setup(
        name='tox-bitbucket-status',
        author='Matthew Schinckel',
        author_email='matt@schinckel.net',
        url='https://bitbucket.org/schinckel/tox-bitbucket-status/',
        description='Update bitbucket status for each env',
        version='1.0',
        py_modules=['tox_bitbucket_status'],
        entry_points={'tox': ['bitbucket_status = tox_bitbucket_status']},
        install_requires=['tox>=2.0', 'requests'],
    )
