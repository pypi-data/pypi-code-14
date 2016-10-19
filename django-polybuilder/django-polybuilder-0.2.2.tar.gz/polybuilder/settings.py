# -*- encoding: utf-8 -*-

from __future__ import unicode_literals

import os
from django.conf import settings

DEFAULT_SKELETON = """<dom-module id="new-component">
    <template>
        <style>
            /* component styles goes here */
            :host {
                display: block;
            }
        </style>

        <!-- local DOM goes here -->
        <span>I'm a {{prop1}}!</span>

    </template>
    <script>
        Polymer({
            is: 'new-component',

            properties: {
                prop1: {
                    type: String,
                    notify: true,
                    value: "new component"
                }
            }
        });
    </script>
</dom-module>
"""

DEFAULT = {
    'POLYMER_SKELETON': DEFAULT_SKELETON,
    'POLYFILL_ENABLED': True,
}


class PolySettings(object):
    """Define PolyBuilder settings and override with
    the django settings dict
    """

    def __init__(self, default, user_settings):
        self.user_settings = self.__get_settings(default, user_settings)

    @staticmethod
    def __get_settings(default, user_settings):
        # Update Default settings with Custom values from user setting
        default.update(getattr(user_settings, 'POLYBUILDER_SETTINGS', DEFAULT))

        # Apply PolyBuilder Settings to Django Settings
        for key, value in default.items():
            setattr(user_settings, key, value)
        return default

    def __getattr__(self, name):
        if name in self.user_settings:
            return self.user_settings[name]
        return super(PolySettings, self).__getattribute__(name)

polysettings = PolySettings(DEFAULT, settings)
