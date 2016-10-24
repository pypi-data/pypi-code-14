# -*- coding: utf-8 -*-

"""
Created on 2016-10-24
:author: Oshane Bailey (b4.oshany@gmail.com)
"""

pytest_plugins = "kotti"

from pytest import fixture


@fixture(scope='session')
def custom_settings():
    import kotti_theme_sbadmin.resources
    kotti_theme_sbadmin.resources  # make pyflakes happy
    return {
        'kotti.configurators': 'kotti_tinymce.kotti_configure '
                               'kotti_theme_sbadmin.kotti_configure'}
