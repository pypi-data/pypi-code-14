# -*- coding: utf-8 -*-
from sys import modules as sysmodules
from pkgutil import walk_packages
from importlib import import_module
from flask import Flask, request
from diandao.flask import SQLAlchemy
import time
import redis


DEFAULT_APP_NAME = "idea"

_vars = {"app": None, "config": {}, "db": None}

# 保存的数据库会话
DB_CONNECTIONS = {}


def create_app(config, app_name=None):
    if app_name is None:
        app_name = DEFAULT_APP_NAME

    app = Flask(app_name)
    if config is None:
        return app
    _vars['app'] = app

    configure_app(app, config)
    configure_db(app)
    configure_redis(app)
    configure_models(app)
    configure_blueprints(app)
    # configure_session(app)
    # configure_auth_handler(app)
    # configure_handler(app)
    # configure_filters(app)
    # #configure_jinja(app)
    # configure_rq(app)
    # configure_sentry(app)


    return app


# ------------
# 应用配置文件
def configure_app(app, config=None):
    # config 不为空时覆盖配置
    if config is not None:
        app.config.from_object(config)

    # 映射配置
    _vars['config'] = app.config


def configure_db(app):
    """
    数据库连接初始化

    :config SQLALCHEMY_POOL_RECYCLE: 连接池生命周期
    :config SQLALCHEMY_POOL_TIMEOUT: 连接池超时
    :config SQLALCHEMY_BINDS: 数据库连接配置, 可配置多个key=>value的配置

    :param app:
    :return:
    """
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy import event, exc, select
    db = SQLAlchemy(app)
    _vars['db'] = db

    @app.teardown_request
    def remove_session(exception=None):
        pass
        #pass
        #db.session.remove()
        #if exception and db.session.is_active:
            #db.session.rollback()


def configure_redis(app):
    """
    Redis 配置, 需要configs.py中的Redis参数

    :config REDIS: (host, port, database)

    :param app:
    :return:
    """
    host, port, db = app.config['REDIS']
    client = redis.Redis(host=host, port=port, db=db)
    app.redisClient = client


# 注册蓝图(Route)
def configure_blueprints(app):
    @app.before_request
    def before_request():
        request.timestamp = time.time()

    import blueprints
    bkeys = []
    prints = []
    for loader, name, is_pkg in walk_packages(blueprints.__path__):
        import_module(blueprints.__name__ + '.' + name)

    for name, blue in blueprints.__dict__.items():
        if hasattr(blue, "blueprint"):
            prints.append((blue.blueprint, getattr(blue, "url_prefix", None)))

    for blue, url_prefix in prints:
        app.register_blueprint(blue, url_prefix=url_prefix)


def configure_models(app):
    import models
    for loader, name, is_pkg in walk_packages(models.__path__):
        import_module(models.__name__ + '.' + name)
        module = getattr(models, name)
        model = getattr(module, name, None)
        if model is None:
            raise ImportError("class %s not found in %s" % (name, module.__file__))
        setattr(models, name, model)

# 获取app配置
def get_config():
    return _vars['config']


# 获取app配置
def get_app():
    return _vars['app']


def get_db():
    return _vars['db']


# 多数据库时, 取到指定数据库连接
def get_db_engine(bind):
    db = get_db()
    app = get_app()
    return db.get_engine(app, bind)


def db_connections():
    return DB_CONNECTIONS


# 初始化数据库
def init_db():
    """
    数据库初始化
    - 未创建表的模型会自动创建数据表
    - 已存在的表, 不会自动更新字段信息

    :return:
    """
    db = get_db()
    db.create_all()



