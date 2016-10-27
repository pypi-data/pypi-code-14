from setuptools import setup, find_packages

setup(
    version='0.3.1',
    name='restipy',
    description=
        '''
            This CLI tool basically uses Jinja2 and the requests
            library to build dynamic requests based on a template
        ''',
    author='Phil Hachey',
    author_email='phil.hachey@bluespurs.com',
    keywords=['rest', 'requests', 'jinja2', 'jmespath', 'template', 'request'],
    package_dir={ '': 'lib' },
    packages=find_packages('lib'),
    install_requires=[
        'requests >= 2.11',
        'pyyaml >= 3.12',
        'jinja2 >= 2.8',
        'jmespath >= 0.9.0',
        'python-jose >= 1.3.2'
    ],
    scripts=[
        'bin/restipy'
    ],
    entry_points={
        'restipy.renderer.plugins': [
            'jwt = restipy.renderer.plugins:jwt',
            'time = restipy.renderer.plugins:time',
            'base64 = restipy.renderer.plugins:base64'
        ],
        'restipy.execution.post': [
            'store = restipy.execution.post.store:StorePostExecutor'
        ],
        'restipy.execution.pre': [
            'store = restipy.execution.pre.store:StorePreExecutor'
        ]
    }
)
