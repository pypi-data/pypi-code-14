from django.conf import settings
from django.db import models

from bulbs.content.models import Content
from bulbs.liveblog.utils import get_liveblog_author_model_name

from .tasks import (firebase_delete_entry,
                    firebase_delete_liveblog,
                    firebase_update_entry)


LIVEBLOG_AUTHOR_MODEL_NAME = get_liveblog_author_model_name()


class AbstractLiveBlog(models.Model):
    """Base mixin inherited by each property's concrete LiveBlog implementation (along with base
    content class).
    """

    pinned_content = models.ForeignKey(Content, blank=True, null=True,
                                       related_name='liveblog_pinned')
    recirc_content = models.ManyToManyField(Content, related_name='liveblog_recirc')

    class Meta:
        abstract = True

    def delete(self, *args, **kwargs):
        firebase_delete_liveblog.delay(liveblog_id=self.id)
        return super(AbstractLiveBlog, self).delete(*args, **kwargs)

    def get_absolute_url(self):
        return '/liveblog/{}-{}'.format(self.slug, self.pk)


class LiveBlogEntry(models.Model):

    liveblog = models.ForeignKey(settings.LIVEBLOG_MODEL, related_name='entries')

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    published = models.DateTimeField(blank=True, null=True)
    authors = models.ManyToManyField(LIVEBLOG_AUTHOR_MODEL_NAME)
    headline = models.CharField(max_length=255, null=True, blank=True)
    body = models.TextField(blank=True)

    recirc_content = models.ManyToManyField(Content, related_name='liveblog_entry_recirc')

    def save(self, *args, **kwargs):
        super(LiveBlogEntry, self).save(*args, **kwargs)
        firebase_update_entry.delay(liveblog_id=self.liveblog.id,
                                    entry_id=self.id,
                                    published=self.published)

    def delete(self, *args, **kwargs):
        firebase_delete_entry.delay(liveblog_id=self.liveblog.id,
                                    entry_id=self.id)
        return super(LiveBlogEntry, self).delete(*args, **kwargs)

    def get_absolute_url(self):
        return '{}?entry={}'.format(self.liveblog.get_absolute_url(), self.pk)

    class Meta:
        ordering = ['-published']


class LiveBlogResponse(models.Model):

    entry = models.ForeignKey(LiveBlogEntry, related_name='responses')
    ordering = models.IntegerField(blank=True, null=True, default=None)

    internal_name = models.CharField(max_length=255, blank=True, null=True)
    author = models.ForeignKey(LIVEBLOG_AUTHOR_MODEL_NAME, blank=True, null=True)
    body = models.TextField(blank=True)

    class Meta:
        ordering = ['ordering']
