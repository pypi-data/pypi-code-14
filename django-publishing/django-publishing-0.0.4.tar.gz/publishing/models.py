# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from publishing import CountryNotAvailableException

SUPERUSER = 'superuser'
ADMINISTRATOR = 'administrator'
NONE = 'none'

PUBLISHING_ROLES = (
    (ADMINISTRATOR, _(u"Administrator")),
    (SUPERUSER, _(u"Superuser")),
    (NONE, _(u"-")),
)

PUBLISHING_LEVELS = {
    ADMINISTRATOR: [ADMINISTRATOR, SUPERUSER],
    SUPERUSER: [SUPERUSER],
    NONE: [],
}


def publisher_can_do(role, level):
    if level in PUBLISHING_LEVELS[role]:
        return True
    return False


class PublishingProfile(models.Model):
    """
    A user profile
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='profile', verbose_name=_("Auth User"), )
    regions = models.ManyToManyField("PublishingRegion", through="PublishingProfileRegion", verbose_name=_(u"Regions"),)

    def can_do(self, obj, level):
        try:
            country = obj.countries
        except CountryNotAvailableException:
            raise CountryNotAvailableException(_(u"%s has no countries field." % (obj.__class__.__name__)))

        return True

    def __str__(self):
        return u"%s" % self.user

    class Meta:
        app_label = 'publishing'
        verbose_name = _(u"Profile")
        verbose_name_plural = _(u"Profiles")
        ordering = ("user", )


class PublishingProfileRegion(models.Model):
    profile = models.ForeignKey("PublishingProfile", verbose_name=_("Profile"), )
    region = models.ForeignKey("PublishingRegion", verbose_name=_("Region"), )
    role = models.CharField(_(u"Role"), max_length=45, default="user", choices=PUBLISHING_ROLES, )

    def __str__(self):
        return u"%s" % _(u"Publishing Region Level")


class PublishingRegion(models.Model):
    title = models.CharField(_(u"Title"), max_length=255, null=True, )
    countries = models.ManyToManyField("PublishingCountry", verbose_name=_(u"Countries"), )
    languages = models.ManyToManyField("PublishingLanguage", verbose_name=_(u"Languages"), )

    def __str__(self):
        return u"%s" % self.title

    class Meta:
        app_label = 'publishing'
        verbose_name = _(u"Region")
        verbose_name_plural = _(u"Regions")
        ordering = ("title", )


class PublishingCountry(models.Model):
    iso_code = models.CharField(_(u"ISO 639-1 Code"), max_length=2, default="en", )
    title = models.CharField(_(u"Title"), max_length=255, null=True, )

    def __str__(self):
        return u"%s" % self.title

    class Meta:
        app_label = 'publishing'
        verbose_name = _(u"Country")
        verbose_name_plural = _(u"Countries")
        ordering = ("title", )


class PublishingLanguage(models.Model):
    iso_code = models.CharField(_(u"ISO 639-1 Code"), max_length=2, default="en", )
    title = models.CharField(_(u"Title"), max_length=255, null=True, )
    models.ManyToManyField("PublishingLanguage", related_name='languages', )

    def __str__(self):
        return u"%s" % self.title

    class Meta:
        app_label = 'publishing'
        verbose_name = _(u"Language")
        verbose_name_plural = _(u"Languages")
        ordering = ("title", )
