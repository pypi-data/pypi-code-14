# -*- coding:utf-8 -*-
import os
import uuid
from six.moves.urllib.parse import urljoin
from django.conf import settings
from django.utils.deconstruct import deconstructible
from django.core.files.storage import Storage

from qiniu import Auth, BucketManager, put_data


@deconstructible
class QiniuStorage(Storage):
    '''
    a storage with qiniu service
    '''

    def __init__(self, bucket_config=None):
        if not bucket_config:
            bucket_config = settings.QINIU_SETTINGS.get('DEFAULT_BUCKET')
        assert bucket_config in settings.QINIU_SETTINGS['BUCKET_CONFIGS']
        assert 'BUCKET_URL' in settings.QINIU_SETTINGS[
            'BUCKET_CONFIGS'][bucket_config]
        assert 'BUCKET_NAME' in settings.QINIU_SETTINGS[
            'BUCKET_CONFIGS'][bucket_config]

        self.access_key = settings.QINIU_SETTINGS['ACCESS_KEY']
        self.secret_key = settings.QINIU_SETTINGS['SECRET_KEY']
        self.bucket_name = settings.QINIU_SETTINGS[
            'BUCKET_CONFIGS'][bucket_config]['BUCKET_NAME']
        self.bucket_url = settings.QINIU_SETTINGS[
            'BUCKET_CONFIGS'][bucket_config]['BUCKET_URL']
        self.bind_url = settings.QINIU_SETTINGS[
            'BUCKET_CONFIGS'][bucket_config].get('BIND_URL', '')
        self.prefix = settings.QINIU_SETTINGS[
            'BUCKET_CONFIGS'][bucket_config].get('PREFIX', '')
        self.is_private_bucket = settings.QINIU_SETTINGS[
            'BUCKET_CONFIGS'][bucket_config].get('IS_PRIVATE', False)
        self.expires_time = settings.QINIU_SETTINGS[
            'BUCKET_CONFIGS'][bucket_config].get('EXPIRES', 3600)

        self.__auth = Auth(self.access_key, self.secret_key)
        self.__bucket_manager = BucketManager(self.__auth)

    def delete(self, name):
        if self.exists(name):
            self.__bucket_manager.delete(self.bucket_name, self.prefix + name)

    def exists(self, name):
        ret, info = self.__bucket_manager.stat(
            self.bucket_name, self.prefix + name)
        return 'hash' in ret

    def path(self, name):
        return self.prefix + name

    def listdir(self, prefix):
        if not prefix:
            prefix = self.prefix
        ret, eof, info = self.__bucket_manager.list(
            self.bucket_name, prefix=prefix)
        return ret

    def size(self, name):
        ret, info = self.__bucket_manager.stat(
            self.bucket_name, self.prefix + name)
        return ret['fsize']

    def url(self, name):
        base_url = self.bind_url or self.bucket_url
        if not self.is_private_bucket:
            return urljoin(base_url, self.path(name))
        else:
            ori_url = urljoin(self.bucket_url, self.path(name))
            return self.__auth.private_download_url(ori_url)

    def put_time(self, name):
        ret, info = self.__bucket.stat(self.bucket_name, self.prefix + name)
        return ret['putTime']

    def save(self, name, content, max_length=None):
        file_name = uuid.uuid1()
        token = self.__auth.upload_token(
            self.bucket_name, self.path(file_name), 3600)
        ret, info = put_data(token, self.path(file_name), content)
        return self.path(file_name)

    def __eq__(self, other):
        return [
            self.access_key == other.access_key,
            self.secret_key == other.secret_key,
            self.bucket_name == other.bucket_name,
            self.prefix == other.prefix,
        ]
