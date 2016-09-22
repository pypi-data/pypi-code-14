#!/usr/bin/env python
# -*- coding: utf-8 -*-
from onyx.core import db
from sqlalchemy.ext.hybrid import hybrid_property


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    admin = db.Column(db.Integer)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(128))
    buttonColor = db.Column(db.String(128))
    registered_on = db.Column(db.DateTime, nullable=False)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    confirmed_on = db.Column(db.DateTime, nullable=True)


    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    def __repr__(self):
        return '<User %r>' % (self.username)
