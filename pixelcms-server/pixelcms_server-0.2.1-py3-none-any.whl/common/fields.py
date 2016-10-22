from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


class LanguageField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 5
        try:
            allow_any = kwargs.pop('allow_any')
        except KeyError:
            allow_any = True
        if allow_any:
            kwargs['choices'] = (('any', '({})'.format(_('any'))),) + \
                settings.LANGUAGES
            kwargs['default'] = 'any'
        else:
            kwargs['choices'] = settings.LANGUAGES
        super(LanguageField, self).__init__(*args, **kwargs)


class FilebrowserVersionField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 255
        kwargs['choices'] = (
            (v, settings.FILEBROWSER_VERSIONS[v]['verbose_name'])
            for v in settings.FILEBROWSER_ADMIN_VERSIONS
        )
        try:
            allow_null = kwargs.pop('allow_null')
        except KeyError:
            allow_null = False
        if allow_null:
            kwargs['null'] = True
            kwargs['blank'] = True
        else:
            if not kwargs.get('default'):
                kwargs['default'] = '3cols'
        super(FilebrowserVersionField, self).__init__(*args, **kwargs)
