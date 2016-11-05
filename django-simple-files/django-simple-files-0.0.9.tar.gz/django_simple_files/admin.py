# -*- coding: UTF-8 -*-
from django.contrib import admin

from django_simple_files import api
from . import models


@admin.register(models.Files)
class FilesAdmin(admin.ModelAdmin):
    list_display = ['file_id','file_name', 'file_uri', 'file_size', 'file_hash', 'enabled',
                    'time_created', 'uploader_uid']
    readonly_fields = ['file_size', 'file_hash', 'uploader_uid']

    def save_model(self, request, obj, form, change):
        file = request.FILES.get('file_uri')
        api.save(file.name, file.read(), request.user.id, obj.file_id if obj.file_id else 0)

