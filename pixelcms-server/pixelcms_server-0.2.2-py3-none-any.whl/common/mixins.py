from django.db import models
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from autoslug import AutoSlugField
from rest_framework import serializers

from .fields import LanguageField


HEADERS_LEVEL_CHOICES = (
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
    ('6', '6'),
)


class TinyMCE:
    js = (
        'https://cdn.tinymce.com/4/tinymce.min.js',
        'admin/tinymce/config.js'
    )


class Module(models.Model):
    name = models.CharField(_('name'), max_length=255)
    published = models.BooleanField(_('published'), default=True)
    template_id = AutoSlugField(
        _('template id'), populate_from='name',
        unique_with='language', editable=True, blank=True
    )
    show_module_name = models.BooleanField(
        _('show module name'), default=True
    )
    module_name_header_level = models.CharField(
        _('module name header level'), max_length=1,
        choices=HEADERS_LEVEL_CHOICES, default='2'
    )
    html_class = models.CharField(
        _('HTML class'), max_length=255, blank=True, default=''
    )
    language = LanguageField(_('language'))

    class Meta:
        abstract = True
        ordering = ('language', 'name')

    def __str__(self):
        return self.name


class ModuleAdmin(admin.ModelAdmin):
    list_display = ('name', 'published', 'template_id', 'language')
    list_filter = ('published', 'language')
    list_editable = ('published', 'language')
    search_fields = ('title', 'template_id')

    fieldsets = [
        (_('Module settings'), {
            'fields': ('name', 'published', 'template_id',
                       ('show_module_name', 'module_name_header_level'),
                       'html_class', 'language')
        })
    ]


class ModuleSerializer(serializers.ModelSerializer):
    def to_representation(self, obj):
        data = super(ModuleSerializer, self).to_representation(obj)
        if not obj.show_module_name:
            data.pop('name')
            data.pop('module_name_header_level')
        if not obj.html_class:
            data.pop('html_class')
        return data


class Seo(models.Model):
    meta_title_override = models.CharField(
        _('page title override'), max_length=255, blank=True, default=''
    )
    meta_title_site_name_suffix = models.NullBooleanField(
        _('site name suffix in page title'), default=None
    )
    meta_description_override = models.CharField(
        _('description override'), max_length=255, blank=True, default=''
    )
    meta_robots_override = models.CharField(
        _('robots override'), max_length=255, blank=True, default=''
    )

    class Meta:
        abstract = True


class SeoAdmin:
    fieldsets = (
        (_('SEO options'), {
            'description': _('Overrides values from <a href="/admin/settings/'
                             'settings/" target="_blank">global settings'
                             '</a>.'),
            'fields': ('meta_title_override',
                       'meta_title_site_name_suffix',
                       'meta_description_override', 'meta_robots_override')
        }),
    )
