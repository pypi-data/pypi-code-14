from distutils.core import setup

setup(
    name='docker-ascii-map',
    version='0.2',
    packages=['docker_ascii_map'],
    package_dir={'': 'src'},
    scripts=['src/docker_ascii_map/docker-ascii-map.py'],
    url='https://github.com/ChessCorp/docker-ascii-map',
    license='MIT',
    author='Yannick Kirschhoffer',
    author_email='alcibiade@alcibiade.org',
    description='A set of python scripts displaying the local docker containers structure and status on an ascii map.'
)
