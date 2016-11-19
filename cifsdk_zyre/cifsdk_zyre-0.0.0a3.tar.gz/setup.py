import os
import sys
from setuptools import setup, find_packages
import versioneer

# vagrant doesn't appreciate hard-linking
if os.environ.get('USER') == 'vagrant' or os.path.isdir('/vagrant'):
    del os.link

# https://www.pydanny.com/python-dot-py-tricks.html
if sys.argv[-1] == 'test':
    test_requirements = [
        'pytest',
    ]
    try:
        modules = map(__import__, test_requirements)
    except ImportError as e:
        err_msg = e.message.replace("No module named ", "")
        msg = "%s is not installed. Install your test requirements." % err_msg
        raise ImportError(msg)
    r = os.system('py.test test -v')
    if r == 0:
        sys.exit()
    else:
        raise RuntimeError('tests failed')

setup(
    name="cifsdk_zyre",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description="CIF Zyre Connector Framework",
    long_description="CIF Zyre Connector Framework",
    url="https://github.com/csirtgadgets/cifsdk-zyre-py",
    license='LGPL3',
    classifiers=[
               "Topic :: System :: Networking",
               "Environment :: Other Environment",
               "Intended Audience :: Developers",
               "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
               "Programming Language :: Python",
               ],
    keywords=['security'],
    author="Wes Young",
    author_email="wes@csirtgadgets.org",
    packages=find_packages(),
    install_requires=[
        'cython>=0.20',
        'cifsdk',
        'pyzyre',
        'pyzmq',
        'csirtg_indicator',
    ],
    scripts=[],
    entry_points={
        'console_scripts': [
            'cif-zyre=cifsdk_zyre.client:main',
        ]
    },
)
