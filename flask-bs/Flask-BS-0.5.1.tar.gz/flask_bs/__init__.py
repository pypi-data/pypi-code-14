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


    Some code copied from:
        https://github.com/maxcountryman/flask-login and https://github.com/mattupstate/flask-security  See LICENSE
"""
from flask import Blueprint, current_app
from jinja2 import Template
from werkzeug.local import LocalProxy
from ._compat import PY2, text_type, iteritems

_bootstrap = LocalProxy(lambda: current_app.extensions['bootstrap'])

_default_config = {
    'SUBDOMAIN': None,
    'URL_PREFIX': None,
    'BLUEPRINT_NAME': 'bootstrap',
}


def get_config(app):
    """Conveniently get the bootstrap configuration for the specified
    application without the annoying 'BOOTSTRAP_' prefix.
    :param app: The application to inspect
    """
    items = app.config.items()
    prefix = 'BOOTSTRAP_'

    def strip_prefix(tup):
        return tup[0].replace('BOOTSTRAP_', ''), tup[1]

    return dict([strip_prefix(i) for i in items if i[0].startswith(prefix)])


def create_blueprint(state, import_name):
    """Creates the navigate extension blueprint

    :param state: Blueprint state object
    :param import_name: Blueprint import name"""

    bp = Blueprint(state.blueprint_name, import_name,
                   url_prefix=state.url_prefix,
                   subdomain=state.subdomain,
                   template_folder='templates')
    return bp


def render_content_with_bootstrap(title='Default', html_language='en', html_attributes='', body_attributes='',
                                  body='Hello world from Flask-BS!', head=''):
    # Future, get a real CDN setup first.
    #             {% if include_flexwidgets_css %}
    #             <link rel="stylesheet" href="https://github.com/bschumacher/Flask-WTF-FlexWidgets/style.css"
    #             crossorigin="anonymous">
    #             {% endif %}
    return Template(
        """
        <!DOCTYPE html>
            <html lang="{{ html_language }}" {{ html_attributes }}>
            <head>
                <meta charset="UTF-8">
                <title>{{ title }}</title>
                <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css"
                 crossorigin="anonymous">
                 {% if not exclude_jquery -%}
                 <script src="http://code.jquery.com/jquery-3.1.1.slim.min.js"
                 crossorigin="anonymous"></script>
                 {% endif -%}
                <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"
                 crossorigin="anonymous"></script>
                {{ head }}
            </head>

            <body {{ body_attributes }}>
                {{ body }}
            </body>
        </html>
        """
    ).render(title=title, html_language=html_language, html_attributes=html_attributes,
             body_attributes=body_attributes, body=body, head=head,
             exclude_jquery=_bootstrap.exclude_jquery)
             # include_flexwidgets_css=_bootstrap.include_flexwidgets_css)


class Bootstrap(object):

    def __init__(self, app=None, **kwargs):
        self.app = app
        self._engine = None
        if app is not None:
            self._state = self.init_app(app, **kwargs)

    def init_app(self, app, register_blueprint=True):

        for key, value in iteritems(_default_config):
            app.config.setdefault('BOOTSTRAP_{key}'.format(key=key), value)

        state = _get_state(app)

        if register_blueprint:
            app.register_blueprint(create_blueprint(state, __name__))

        app.extensions['bootstrap'] = state

        return state

    def __getattr__(self, name):
        return getattr(self._state, name, None)


def _get_state(app, **kwargs):
    for key, value in iteritems(get_config(app)):
        kwargs[key.lower()] = value

    kwargs.update(
        dict(
            app=app,
        )
    )

    return _BootstrapState(**kwargs)


class _BootstrapState(object):

    def __init__(self, **kwargs):
        self.blueprint_name = 'bootstrap'
        self.url_prefix = None
        self.subdomain = None
        self.exclude_jquery = False
        for key, value in iteritems(kwargs):
            setattr(self, key.lower(), value)
