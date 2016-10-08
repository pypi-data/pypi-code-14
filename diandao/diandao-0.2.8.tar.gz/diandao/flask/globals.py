# -*- coding: utf-8 -*-

from functools import partial
from werkzeug.local import LocalStack, LocalProxy
from flask_redis import FlaskRedis
from flask_sqlalchemy import SQLAlchemy
from flask_rq import RQ
from celery import Celery

redis = FlaskRedis()
db = SQLAlchemy()
celery = Celery()
rq = RQ()

stacker = {
    "app": None
}

def _lookup_(name):
    return stacker[name]

app=LocalProxy(partial(_lookup_,"app"))