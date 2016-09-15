#!/usr/bin/env python
# -*- coding: utf-8 -*-
from onyx.core import db


class Calendar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    idAccount = db.Column(db.String(64))
    title = db.Column(db.String(64))
    start = db.Column(db.String(64))
    end = db.Column(db.String(64))
    color = db.Column(db.String(64))
    allday = db.Column(db.String(64))


    @property
    def is_active(self):
        return True

    def get_id_(self):
        try:
            return unicode(self.id)  
        except NameError:
            return str(self.id)  
