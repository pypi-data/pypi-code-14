# -*- coding: utf-8 -*-

from thumbor import storages
from tornado.concurrent import return_future

from pgthumbor import models


class Storage(storages.BaseStorage):

    @staticmethod
    def get_image(path):
        return models.Image.get(path)

    @staticmethod
    def save_db(image):
        image.save()

    @return_future
    def get(self, path, callback):
        image = self.get_image(path)
        if not image:
            callback(None)
            return
        callback(image.decoded_data)

    def put(self, path, data):
        image = self.get_image(path)
        if not image:
            image = models.Image()
        image.set_values(path, data)
        return path

    def remove(self, path):
        image = self.get_image(path)
        if image:
            image.delete()

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
            image.set_crypto(self.context.server.security_key)
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
            image.set_detector(data)
        return path
