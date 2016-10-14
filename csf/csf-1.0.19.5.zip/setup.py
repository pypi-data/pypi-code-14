# coding=utf-8
import os.path

import setuptools

import csf

here = os.path.abspath(os.path.dirname(__file__))

long_description = """
csf
===

Installation
------------
    pip install csf

Upgrade
-------
	pip install csf --upgrade

Quick Start
-----------
::

    import csf
    csf.config.set_token("ACCESS_KEY","SECRET_KEY") 设置token
    csf.get_stock_hist_bar(code="000001")

"""

name = "csf"
description = "Python module to get stock data from chinascope"
version = csf.__version__
author = "chinascope"
author_email = "it@chinascopefinancial.com"
home_page = "http://api.ichinascope.com"
download_url = "http://qiniu.csfimg.com/sdk/csf-%s.zip" % csf.__version__

setuptools.setup(
    name=name,
    packages=[name],
    version=version,
    description=description,
    author=author,
    license='BSD',
    author_email=author_email,
    url=home_page,
    download_url=download_url,
    keywords=('csf', 'stock', 'data', 'chinascope'),
    classifiers=[
        # How mature is this project? Common values are
        # 3 - Alpha
        # 4 - Beta
        # 5 - Production/Stable
        'Development Status :: 5 - Production/Stable',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Intended Audience :: Financial and Insurance Industry',
        'Topic :: Office/Business :: Financial :: Investment',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Operating System :: OS Independent',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: BSD License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    long_description=long_description
)
