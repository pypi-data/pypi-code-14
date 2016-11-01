import src
from src.packer import Packer

packer = Packer()
packer.loadLongDescription('README')
packer.pickPackage('pyckax', 'src')
packer.setup(
    name='pyckax',
    version=src.__version__,
    description='a python scrape tool',
    url='https://github.com/chaosannals/pythax',
    keywords='pyckax python package',
    license='MIT',
    author='chaosannals',
    author_email='chaosannals@outlook.com',
    classifiers= [
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython'
    ],
    include_package_data=True,
    zip_safe=True,
    platforms='any'
)
