# -*- coding: utf-8 -*-
"""
    Flask-Pages - Another? flask extension that provides dynamic pages.

    Author: Bill Schumacher <bill@servernet.co>
    License: LGPLv3
    Copyright: 2016 Bill Schumacher, Cerebral Power
** GNU Lesser General Public License Usage
** This file may be used under the terms of the GNU Lesser
** General Public License version 3 as published by the Free Software
** Foundation and appearing in the file LICENSE.LGPLv3 included in the
** packaging of this file. Please review the following information to
** ensure the GNU Lesser General Public License version 3 requirements
** will be met: https://www.gnu.org/licenses/lgpl.html.
"""
from setuptools import setup, find_packages

requirements = ['Flask', 'Flask-BS', 'Flask-Security', 'Flask-SQLAlchemy']


setup(
    name="Flask-Pages",
    version="0.1.0",
    author="Bill Schumacher",
    author_email="bill@servernet.co",
    description="Another? flask extension that provides dynamic pages.",
    license="LGPLv3",
    keywords="flask page wysiwyg dynamic",
    url="https://github.com/bschumacher/Flask-Pages",
    install_requirements=requirements,
    packages=find_packages(),
    setup_requires=[],
    tests_require=[],
)
