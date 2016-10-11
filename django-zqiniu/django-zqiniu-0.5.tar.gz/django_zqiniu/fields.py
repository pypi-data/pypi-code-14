#-*- coding:utf-8 -*-

from django.db.models.fields.files import FileField, ImageField


class QiniuFileField(FileField):
    def __init__(self, *args, **kwargs):
        super(QiniuFileField, self).__init__(*args, **kwargs)


class QiniuImageField(ImageField):
    def __init__(self, *args, **kwargs):
        super(QiniuImageField, self).__init__(*args, **kwargs)
