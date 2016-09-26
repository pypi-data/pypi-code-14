from setuptools import setup

import io
import umodules.umodules as umodules


def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)


long_description = read('README.rst', 'CHANGES.txt')

required = [
    'markdown',
    'pyyaml',
    'gitpython',
    'progress',
    'yapsy',
    'munch',
    'dotmap',
    'wget'
]

extras = {
    'develop': [
        'pytest',
        'nose'
    ]
}

setup(

    name='umodules',
    version=umodules.__version__,
    description='Organize your Unity Projects with uModules',
    url='https://gitlab.com/umodules/umodules',
    author='sP0CkEr2',
    author_email='paul@spocker.net',
    license='MIT',
    packages=['umodules', 'umodules.commands', 'umodules.module_types'],
    package_data={'umodules.commands': ['*.plugin'], 'umodules.module_types': ['*.plugin']},
    install_requires=required,
    extras_required=extras,
    zip_safe=True,
    test_suite='nose.collector',
    tests_require=['nose'],
    entry_points={
        'console_scripts': ['umodules=umodules.umodules:main'],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Utilities',
        'Topic :: Games/Entertainment'
    ]
)
