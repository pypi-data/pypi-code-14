# -*- coding: utf-8 -*-
# Created by lvjiyong on 16/8/20
import logging

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django_simple_files.models import Files

logger = logging.getLogger('django')


def save(name, content, storage_instance=None):
    """
    使用django storage 保存文件
    :param storage_instance:
    :param name:
    :param content:
    :return:
    """

    if isinstance(storage_instance, Files):
        storage_instance.file_uri.save(name, ContentFile(content))
        return storage_instance.file_uri.name
    elif not storage_instance:
        logger.debug(storage_instance)
        storage_instance = default_storage
    return storage_instance.save(name, ContentFile(content))


def exists(name):
    return default_storage.exists(name)


def delete(name):
    return default_storage.delete(name)
