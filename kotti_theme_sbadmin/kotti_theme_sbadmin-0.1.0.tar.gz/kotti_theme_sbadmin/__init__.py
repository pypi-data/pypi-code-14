# -*- coding: utf-8 -*-

"""
Created on 2016-10-24
:author: Oshane Bailey (b4.oshany@gmail.com)
"""

import pkg_resources
from kotti.views.util import TemplateAPI as KottiTemplateAPI
from pyramid.i18n import TranslationStringFactory

_ = TranslationStringFactory('kotti_theme_sbadmin')


class ThemeConfig(object):

    @classmethod
    def version(cls):
        return TemplateAPI.version


class TemplateAPI(KottiTemplateAPI):
    version = ""


def kotti_configure(settings):
    """ Add a line like this to you .ini file::

            kotti.configurators =
                kotti_theme_sbadmin.kotti_configure

        to enable the ``kotti_theme_sbadmin`` add-on.

    :param settings: Kotti configuration dictionary.
    :type settings: dict
    """

    settings["kotti.templates.api"] = 'kotti_theme_sbadmin.TemplateAPI'
    settings['pyramid.includes'] += ' kotti_theme_sbadmin'
    settings['kotti.fanstatic.view_needed'] += ' kotti_theme_sbadmin.fanstatic.css_and_js'


def includeme(config):
    """ Don't add this to your ``pyramid_includes``, but add the
    ``kotti_configure`` above to your ``kotti.configurators`` instead.

    :param config: Pyramid configurator object.
    :type config: :class:`pyramid.config.Configurator`
    """

    config.add_translation_dirs('kotti_theme_sbadmin:locale')
    config.override_asset('kotti', 'kotti_theme_sbadmin:overrides/kotti/')
    config.add_static_view('static-kotti_theme_sbadmin', 'kotti_theme_sbadmin:static')
    TemplateAPI.version = \
        pkg_resources.get_distribution("kotti_theme_sbadmin").version
