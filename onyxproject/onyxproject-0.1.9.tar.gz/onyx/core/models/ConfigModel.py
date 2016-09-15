#!/usr/bin/env python
# -*- coding: utf-8 -*-
from onyx.core import db


class Config(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    value = db.Column(db.String(64))


    @property
    def is_active(self):
        return True

    def get_id_(self):
        try:
            return unicode(self.id)  
        except NameError:
            return str(self.id)  
