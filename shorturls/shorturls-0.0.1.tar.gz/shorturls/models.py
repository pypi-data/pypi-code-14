# -*- coding: utf-8 -*-

import logging

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from .utils.nonce import nonce_factory

logger = logging.getLogger(__name__)


class Url(models.Model):
    url = models.URLField(
        _('URL'), max_length=4096, default='', blank=False, unique=True)
    code = models.CharField(
        _('code'), max_length=16, blank=True, unique=True, db_index=True)
    counter = models.PositiveIntegerField(_('counter'), default=0)
    date_created = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = _('URL')
        verbose_name_plural = _('URLs')

    def log(self, content='viewed'):
        """
        This is a use-counter. Only call this method on use.
        """
        logger.info('URL:{0} - [{1}]'.format(self.code, content))
        self.counter += 1
        self.save()

    def save(self, **kwargs):
        """
        Assigns a Nonce if this object does not yet have one.
        """
        code_length = getattr(settings, 'SHORTURLS_CODE_LENGTH', 6)
        while not self.code:
            code = nonce_factory.get_nonce(chars=code_length)
            if not Url.objects.filter(code=code).exists():  # pragma: no cover
                self.code = code
        return super(Url, self).save(**kwargs)

    def get_short_url(self):
        """
        Returns the short URL.
        """
        return reverse(
            'shorturls:redirect_url', kwargs={'code': self.code})

    def get_absolute_url(self):
        """
        Returns the original, unshortened URL.
        """
        return self.url
