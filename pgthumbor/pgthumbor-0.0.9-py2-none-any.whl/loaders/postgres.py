# -*- coding: utf-8 -*-

from thumbor.loaders import LoaderResult
from tornado.concurrent import return_future

from pgthumbor import models


@return_future
def load(context, path, callback):
    image = models.Image.get(path)
    result = LoaderResult()
    if image:
        result.successful = True
        result.buffer = image.decoded_data
    else:
        result.successful = False
        result.error = LoaderResult.ERROR_NOT_FOUND
    callback(result)
