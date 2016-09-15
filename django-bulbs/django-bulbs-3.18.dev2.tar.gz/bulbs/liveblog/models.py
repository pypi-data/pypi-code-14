from django.conf import settings
from django.db import models
from django.utils import timezone

from bulbs.content.models import Content
from bulbs.liveblog.utils import get_liveblog_author_model_name


class AbstractLiveBlog(models.Model):
    """Base mixin inherited by each property's concrete LiveBlog implementation (along with base
    content class).
    """

    pinned_content = models.ForeignKey(Content, blank=True, null=True,
                                       related_name='liveblog_pinned')
    recirc_content = models.ManyToManyField(Content, related_name='liveblog_recirc')

    class Meta:
        abstract = True

    def entries_page(self, after_entry=None):
        entries_query = self.entries.order_by('published')
        if after_entry:
            entries_query = entries_query.filter(
                published__lte=timezone.now(),
                published__gt=after_entry.published)
        else:
            entries_query = entries_query.filter(
                published__lte=timezone.now())
        return entries_query[:10]

    def get_absolute_url(self):
        return '/liveblog/{}-{}'.format(self.slug, self.pk)


class LiveBlogEntry(models.Model):

    liveblog = models.ForeignKey(settings.BULBS_LIVEBLOG_MODEL, related_name='entries')

    published = models.DateTimeField(blank=True, null=True)
    authors = models.ManyToManyField(get_liveblog_author_model_name())
    headline = models.CharField(max_length=255, null=True, blank=True)
    body = models.TextField(blank=True)

    recirc_content = models.ManyToManyField(Content, related_name='liveblog_entry_recirc')

    def get_absolute_url(self):
        return '{}?entry={}'.format(self.liveblog.get_absolute_url(), self.pk)


class LiveBlogResponse(models.Model):

    entry = models.ForeignKey(LiveBlogEntry, related_name='responses')
    ordering = models.IntegerField(blank=True, null=True, default=None)

    internal_name = models.CharField(max_length=255, blank=True, null=True)
    author = models.ForeignKey(get_liveblog_author_model_name(), blank=True, null=True)
    body = models.TextField(blank=True)

    class Meta:
        ordering = ['ordering']
