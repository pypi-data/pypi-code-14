from setuptools import setup, find_packages

setup(
    name='triptan',
    version='1.0.4',
    description='Datastore independent migration tool',
    author='Alexander Jung-Loddenkemper',
    author_email='alexander@julo.ch',
    url='https://github.com/alexanderjulo/triptan',
    packages=find_packages(),
    package_data={
        'triptan': ['templates/*.jinja2']
    },
    install_requires=[
        'Click>=6,<7',
        'click-log<1',
        'PyYAML>=3,<4',
        'jinja2>=2,<4'
    ],
    tests_require=['pytest'],
    entry_points={
        'console_scripts': ['triptan=triptan.cli:main']
    }
)
