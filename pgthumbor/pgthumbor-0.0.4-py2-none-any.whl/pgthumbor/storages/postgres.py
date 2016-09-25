import os

import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from thumbor import storages
from tornado.concurrent import return_future

Base = declarative_base()
engine = db.create_engine(os.environ['DATABASE_URL'])
Session = sessionmaker(bind=engine)


class Image(Base):
    __tablename__ = 'images'
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(), unique=True, nullable=False)
    data = db.Column(db.Text(), nullable=False)
    detector = db.Column(db.Text(), nullable=True)
    crypto = db.Column(db.Text(), nullable=True)


class Storage(storages.BaseStorage):
    def __init__(self, context):
        super(Storage, self).__init__(context)
        self.session = Session()

    def get_image(self, path):
        return self.session.query(Image).filter(Image.path == path).first()

    def save_db(self, image):
        self.session.add(image)
        self.session.commit()

    @return_future
    def get(self, path, callback):
        image = self.get_image(path)
        if not image:
            callback(None)
            return
        callback(image.data)

    def put(self, path, bytes):
        image = self.get_image(path)
        if not image:
            image = Image()
        image.path = path
        image.data = bytes
        self.save_db(image)
        return path

    def remove(self, path):
        image = self.get_image(path)
        if image:
            self.session.delete(image)
            self.session.commit()

    @return_future
    def exists(self, path, callback):
        image = self.get_image(path)
        callback(image is not None)

    @return_future
    def get_crypto(self, path, callback):
        image = self.get_image(path)
        if image:
            callback(image.crypto)
            return
        callback(None)

    def put_crypto(self, path):
        if not self.context.config.STORES_CRYPTO_KEY_FOR_EACH_IMAGE:
            return
        if not self.context.server.security_key:
            raise RuntimeError("STORES_CRYPTO_KEY_FOR_EACH_IMAGE can't be True if no SECURITY_KEY specified")
        image = self.get_image(path)
        if image:
            image.crypto = self.context.server.security_key
            self.save_db(image)
        return path

    @return_future
    def get_detector_data(self, path, callback):
        image = self.get_image(path)
        if image:
            callback(image.detector)
            return
        callback(None)

    def put_detector_data(self, path, data):
        image = self.get_image(path)
        if image:
            image.detector = data
            self.save_db(image)
        return path
