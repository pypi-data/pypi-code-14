from flask import Flask
from bucket.config.default_settings import DefaultConfig


def create_app(name, config=None, flask_params=None):
    """ Creates app """
    options = dict(import_name=name)

    if flask_params is not None:
        options.update(flask_params)

    app = Flask(**options)
    configure_app(app, config)
    return app


def add_orm(app):
    """ Add SQLAlchemy ORM integration """
    from bucket.feature.orm import orm_feature
    orm_feature(app)


def configure_app(app, config=None):
    """ Configures app """
    if config is None:
        config = DefaultConfig()

    if config.__class__ is type:
        raise Exception('Config must be an object')

    app.config.from_object(config)


def add_debug_toolbar(app):
    """ Add debug toolbar """
    from bucket.feature.debug_toolbar import debug_toolbar_feature
    debug_toolbar_feature(app)
