from django.db import models
from django.utils.translation import ugettext_lazy as _

from cms.common.fields import LanguageField


class Settings(models.Model):
    language = LanguageField(_('language'), unique=True)
    site_name = models.CharField(
        _('site name'), max_length=255
    )
    page_title_site_name_suffix = models.BooleanField(
        _('site name suffix in page title'), default=True
    )
    suffix_separator = models.CharField(
        _('suffix separator'), max_length=10, default='|'
    )
    meta_description = models.CharField(
        _('description'), max_length=255, blank=True, default=''
    )
    meta_robots = models.CharField(
        _('robots'), max_length=255, blank=True, default='index, follow'
    )

    class Meta:
        app_label = 'settings'
        ordering = ('language',)
        verbose_name = _('general settings')
        verbose_name_plural = _('general settings')

    def __str__(self):
        return self.language
