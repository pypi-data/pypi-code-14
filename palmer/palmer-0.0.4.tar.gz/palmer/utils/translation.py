# -*- coding:utf-8 -*-
from flask import current_app
from speaklater import make_lazy_gettext

from palmer.config import default_config


def _lazy_gettext():
    def _(s):
        config = current_app.api_config if current_app else default_config
        return getattr(config, 'GETTEXT_FUNC')(s)
    return _

lazy_gettext = make_lazy_gettext(_lazy_gettext)
