# -*- coding: UTF-8 -*-

from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.utils import timezone

from django_simple_files.utils import get_upload_to


class Files(models.Model):
    """
    文件DB存储数据
    """

    class Meta:
        verbose_name_plural = '文件存档'
        verbose_name = '文件存档'
        ordering = ['-file_id']

    file_name = models.CharField('文件名', max_length=255)
    file_id = models.AutoField('ID', primary_key=True)
    file_uri = models.FileField('文件', max_length=255, upload_to=get_upload_to(),)
    file_size = models.BigIntegerField('文件大小', default=0)
    file_hash = models.CharField('文件hash', max_length=40)
    time_created = models.DateTimeField('上传时间', default=timezone.now)
    uploader_uid = models.IntegerField('上传者UID', default=0)
    enabled = models.BooleanField('使用中', default=True)

    def __unicode__(self):
        return self.file_uri.name

    def __str__(self):
        return self.file_uri.name


@receiver(post_delete, sender=Files)
def delete_file_handle(sender, **kwargs):
    """
    绑定删除事件
    :param sender:
    :param kwargs:
    :return:
    """
    _instance = kwargs.get('instance')
    _instance.file_uri.delete(save=False)


class FilesRelated(models.Model):
    """
    文件关系存储数据
    """

    class Meta:
        verbose_name_plural = '文件关系存储'
        verbose_name = '文件关系存储'
        ordering = ['-related_id']

    related_id = models.AutoField('ID', primary_key=True)
    file = models.ForeignKey(Files)
    file_uri = models.CharField('文件', max_length=255)
    related_object_id = models.CharField('对象PK', max_length=191, db_index=True)
    related_object = models.CharField('对象名', max_length=100, db_index=True)
    time_created = models.DateTimeField('上传时间', default=timezone.now)

    def __unicode__(self):
        return self.file_uri

    def __str__(self):
        return self.file_uri


