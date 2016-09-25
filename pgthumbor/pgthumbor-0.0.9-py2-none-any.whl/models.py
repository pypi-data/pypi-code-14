# -*- coding: utf-8 -*-

import os
import base64

import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = db.create_engine(os.environ['DATABASE_URL'])
Session = sessionmaker(bind=engine)


class Image(Base):
    __tablename__ = 'images'
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(), unique=True, nullable=False)
    data = db.Column(db.UnicodeText(), nullable=False)
    detector = db.Column(db.Text(), nullable=True)
    crypto = db.Column(db.Text(), nullable=True)
    session = Session()

    @classmethod
    def get(cls, path):
        return cls.session.query(cls).filter(cls.path == path).first()

    @property
    def decoded_data(self):
        return base64.b64decode(self.data)

    def set_values(self, path, data):
        self.path = path
        self.data = base64.b64encode(data)
        self.save()

    def set_detector(self, detector):
        self.detector = detector
        self.save()

    def set_crypto(self, crypto):
        self.crypto = crypto
        self.save()

    def save(self):
        Image.session.add(self)
        Image.session.commit()

    def delete(self):
        Image.session.delete(self)
        Image.session.commit()
