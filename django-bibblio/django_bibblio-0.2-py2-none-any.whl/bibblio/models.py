# -*- coding: utf-8 -*-
import collections
import uuid
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from jsonfield import JSONField


class BibblioIDMapManager(models.Manager):
    """
    Adds some extra methods for getting records
    """
    def get_for_instance(self, model):
        """
        Return a BibblioID object from a model instance
        """
        ctype = ContentType.objects.get_for_model(model)
        return self.get_queryset().get(content_type=ctype, object_id=model.pk)


class BibblioIDMap(models.Model):
    """
    A map from a content item to a Bibblio ID
    """
    bibblio_id = models.UUIDField(
        _('Bibblio ID'),
        default=uuid.uuid4,
        db_index=True)
    content_type = models.ForeignKey(ContentType, related_name="bibblio_id_maps")
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    objects = BibblioIDMapManager()

    class Meta:
        verbose_name = _("Bibblio ID Map")
        verbose_name_plural = _("Bibblio ID Maps")
        unique_together = ('bibblio_id', 'content_type', 'object_id', )

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        return unicode(self.bibblio_id)


class Metadata(models.Model):
    """
    Keywords and Entity metadata
    """
    text = models.CharField(
        _('text'),
        max_length=255)
    type = models.CharField(
        _('type'),
        max_length=255,
        default='Keyword',
        db_index=True)
    linked_data = JSONField(
        _('linked data'),
        load_kwargs={'object_pairs_hook': collections.OrderedDict},
        default="{}")
    ignore = models.BooleanField(
        _('ignore'),
        default=False,
        help_text=_('When true, content is never tagged with this metadata, and '
            'remove from previously tagged content.'))

    class Meta:
        verbose_name = _("Metadata")
        verbose_name_plural = _("Metadata")
        unique_together = ('text', 'type', )
        index_together = ['text', 'type', ]
        ordering = ('type', 'text')

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        return "%s (%s)" % (self.text, self.type)

    def save(self, *args, **kwargs):
        """
        If ignore is True, delete previous connections
        """
        if self.ignore:
            self.contentmetadata_set.all().delete()
        super(Metadata, self).save(*args, **kwargs)


class ContentMetadata(models.Model):
    """
    Link of content and metadata
    """
    content_type = models.ForeignKey(ContentType, related_name="+")
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    bibblio_id = models.ForeignKey(BibblioIDMap)
    metadata = models.ForeignKey(Metadata)
    relevance = models.FloatField(
        _('relevance'),
        default=0.0)
    count = models.PositiveIntegerField(_('count'), default=0)
    additional_data = JSONField(
        _('additional data'),
        load_kwargs={'object_pairs_hook': collections.OrderedDict},
        default="{}")
    ignore = models.BooleanField(
        _('ignore'),
        default=False,
        help_text=_('When true, this content is never tagged with this metadata.'))

    class Meta:
        verbose_name = _("Content Metadata")
        verbose_name_plural = _("Content Metadata")

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        return u"%s %s %s" % (self.content_object, self.bibblio_id, self.relevance)


class QueuedContent(models.Model):
    """
    Content that is queued up to get indexed
    """
    content_type = models.ForeignKey(ContentType, related_name="+")
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    bibblio_id = models.ForeignKey(BibblioIDMap, blank=True, null=True)
    status = models.CharField(
        _('status'),
        max_length=50,
        default='index',
        choices=(
            ('index', _('To Index')),
            ('get_results', _('Awaiting Results')),
            ('error', _('An Error Occurred')),
            ('done', _('Finished'))))
    status_info = models.TextField(
        _('status information'),
        blank=True,
        default='')

    class Meta:
        verbose_name = _("QueuedContent")
        verbose_name_plural = _("QueuedContent")
