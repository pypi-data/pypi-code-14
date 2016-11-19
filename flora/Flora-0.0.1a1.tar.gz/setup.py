from setuptools import setup, find_packages
from os import path
here = path.abspath(path.dirname(__file__))
requirements = open(path.join(here, 'requirements.txt'), 'r').readlines()
# import version # Get Flora's Version (Disabled For Now)

setup(
    name='Flora',
    version='0.0.1a1',
    description='Flora',
    url='https://fuzen-py.github.io/Flora/',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3 :: Only',],
    install_requires=requirements,
    packages = ['Flora', 'Flora.utils', 'Flora.commands'],
    package_data={'Flora.utils':['config/*', 'config/Plugins/*',
                                 'config/Plugins/Plugin/*',
                                 'config/Data/*']},
    include_package_data=True,
    entry_points={'console_scripts': ['flora-run=Flora:run']},
    zip_safe=False
)
