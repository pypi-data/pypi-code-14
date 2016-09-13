from setuptools import setup, find_packages

setup(
    name='triptan',
    version='1.0.1',
    description='Datastore independent migration tool',
    author='Alexander Jung-Loddenkemper',
    author_email='alexander@julo.ch',
    url='https://github.com/alexanderjulo/triptan',
    packages=find_packages(),
    install_requires=[
        'Click==6',
        'click-log==0',
        'PyYAML==3',
        'jinja2==2'
    ],
    tests_require=['pytest'],
    entry_points={
        'console_scripts': ['triptan=triptan.cli:main']
    }
)
