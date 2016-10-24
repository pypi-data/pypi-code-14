# -*- coding: utf-8 -*-

"""
Created on 2016-10-24
:author: Oshane Bailey (b4.oshany@gmail.com)
"""

from __future__ import absolute_import

from fanstatic import Group
from fanstatic import Library
from fanstatic import Resource


library = Library("kotti_theme_sbadmin", "static")

css = Resource(
    library,
    "styles.css")
js = Resource(
    library,
    "scripts.js")

css_and_js = Group([css, js])
