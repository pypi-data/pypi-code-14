# -*- coding: utf-8 -*-

from flask import redirect, url_for, session, request, jsonify
from flask_nemo.plugin import PluginPrototype
from pkg_resources import resource_filename
from nemo_oauth_plugin import NemoOauthPlugin


class PerseusNemoUi(PluginPrototype):
    """
        The Breadcrumb plugin is enabled by default in Nemo.
        It can be overwritten or removed. It simply adds a breadcrumb

    """
    HAS_AUGMENT_RENDER = False
    TEMPLATES = {"main": resource_filename("perseus_nemo_ui", "data/templates")}
    CSS = [resource_filename("perseus_nemo_ui","data/assets/css/theme-ext.css")]
    STATICS = [
        resource_filename("perseus_nemo_ui","data/assets/images/rev_running_man.png")
    ]
    ROUTES = [("/test","r_test",["GET"])]

    def __init__(self, *args, **kwargs):
        super(PerseusNemoUi, self).__init__(*args, **kwargs)


    @NemoOauthPlugin.oauth_required
    def r_test(self):
        return { "template": "main::index.html" }

