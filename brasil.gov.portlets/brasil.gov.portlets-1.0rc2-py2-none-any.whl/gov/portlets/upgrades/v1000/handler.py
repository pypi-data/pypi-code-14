# -*- coding: utf-8 -*-
from brasil.gov.portlets.config import PROJECTNAME
from plone import api
from plone.app.upgrade.utils import loadMigrationProfile

import logging


def apply_profile(context):
    """Atualiza perfil para versao 1000."""
    logger = logging.getLogger(PROJECTNAME)
    profile = 'profile-brasil.gov.portlets.upgrades.v1000:default'
    loadMigrationProfile(context, profile)
    register_vendor_js()
    logger.info('Atualizado para versao 1000')


def register_vendor_js():
    """Check if vendor JS are already registered,
       if not register it
    """
    JS_TO_REGISTER = [
        'jquery.cycle2.js',
        'jquery.cycle2.carousel.js',
        'jquery.jplayer.min.js'
    ]

    js_tool = api.portal.get_tool('portal_javascripts')
    for js in JS_TO_REGISTER:
        find_js = False
        for id in js_tool.getResourceIds():
            find_js = (js in id)
            if find_js:
                break
        if not find_js:
            js_tool.registerResource(
                '++resource++brasil.gov.portlets/js/{0}'
                .format(js))
            js_tool.moveResourceBefore(
                '++resource++brasil.gov.portlets/js/{0}'
                .format(js),
                '++resource++brasil.gov.portlets/js/main.js')
    js_tool.cookResources()
