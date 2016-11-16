# -*- coding:utf-8 -*-
from flask import current_app
from speaklater import make_lazy_gettext

from palmer.config import default_config

config = current_app.api_config if current_app else default_config
lazy_gettext = make_lazy_gettext(lambda: getattr(config, 'GETTEXT_FUNC'))
