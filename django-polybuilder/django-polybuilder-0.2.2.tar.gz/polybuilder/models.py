# -*- encoding: utf-8 -*-

from __future__ import unicode_literals

import os
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.db import models
from .settings import polysettings
from .utils import get_bower_choices


@python_2_unicode_compatible
class ComponentTypeMixin(models.Model):
    """Mixin for defining the component type"""

    STYLES = 10
    COMPONENT = 20
    COMPOUND = 30
    APP_SPECIFIC = 40

    TYPE_CHOICES = (
        (STYLES, _('Styles')),
        (COMPONENT, _('Component')),
        (COMPOUND, _('Compound')),
        (APP_SPECIFIC, _('App Specific')),
    )

    component_type = models.IntegerField(
        default=COMPONENT,
        choices=TYPE_CHOICES,
        verbose_name=_('type'),
    )

    class Meta:
        abstract = True
        verbose_name = _('Content Type')
        verbose_name_plural = _('Content Types')


@python_2_unicode_compatible
class Component(ComponentTypeMixin):
    """Polymer component"""

    slug = models.SlugField(
        unique=True,
        verbose_name=_('slug'),
    )
    code = models.TextField(
        default=polysettings.POLYMER_SKELETON,
        blank=True, null=True,
        verbose_name=_('code'),
    )
    is_main = models.BooleanField(
        default=False,
        verbose_name=_('is main'),
    )

    def save(self):
        if self.is_main:
            Component.objects.filter(is_main=True).update(is_main=False)
        super(Component, self).save(False, False, None, None)

    class Meta:
        verbose_name = _('Component')
        verbose_name_plural = _('Components')
        ordering = ('component_type', 'is_main')

    def __str__(self):
        return '<{}>'.format(self.slug)


@python_2_unicode_compatible
class Dependency(models.Model):
    """Bower installed dependencies"""

    HTML = 'HTML'
    CSS = 'CSS'
    JS = 'JS'

    DEPENDENCY_TYPE_CHOICES = (
        (HTML, _('HTML')),
        (CSS, _('CSS')),
        (JS, _('JavaScript')),
    )

    name = models.CharField(
        max_length=255,
        verbose_name=_('name'),
    )
    path = models.CharField(
        max_length=1024,
        choices=get_bower_choices(),
        verbose_name=_('path'),
    )
    dependency_type = models.CharField(
        default=HTML,
        max_length=16,
        choices=DEPENDENCY_TYPE_CHOICES,
        verbose_name=_('type')
    )
    ordering = models.IntegerField(
        default=0,
        verbose_name=_('ordering'),
    )

    def __str__(self):
        return '{}: {}'.format(self.name, self.dependency_type)

    class Meta:
        verbose_name = _('Dependency')
        verbose_name_plural = _('Dependencies')
        ordering = ('ordering',)
