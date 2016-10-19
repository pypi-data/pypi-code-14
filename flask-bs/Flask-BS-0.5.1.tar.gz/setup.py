# -*- coding: utf-8 -*-
"""
    Flask-BS - Another flask extension that provides Bootstrap CSS, JS and HTML5 boilerplate.

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

requirements = ['Flask']


setup(
    name="Flask-BS",
    version="0.5.1",
    author="Bill Schumacher",
    author_email="bill@servernet.co",
    description="Another flask extension that provides Bootstrap CSS, JS and HTML5 boilerplate.",
    license="LGPLv3",
    keywords="flask bootstrap html5 boilerplate",
    url="https://github.com/bschumacher/Flask-BS",
    install_requirements=requirements,
    packages=find_packages(),
    setup_requires=[],
    tests_require=[],
)
