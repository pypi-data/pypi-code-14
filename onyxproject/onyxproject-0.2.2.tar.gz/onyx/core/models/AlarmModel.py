#!/usr/bin/env python
# -*- coding: utf-8 -*-
from onyx.core import db


class Alarm(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String(64))
    ring = db.Column(db.String(64))
    heure = db.Column(db.String(120))
    active = db.Column(db.String(64))

    @property
    def is_active(self):
        return True

    def get_id_(self):
        try:
            return unicode(self.id)  
        except NameError:
            return str(self.id)  
