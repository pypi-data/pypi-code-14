from django.db import models
from django.utils.translation import ugettext_lazy as _
from photologue.models import Photo
from django.http import HttpResponseRedirect
from hvad.models import TranslatableModel, TranslatedFields
from django.core.urlresolvers import reverse


class Article(TranslatableModel):
    slug = models.SlugField(_('Slug'), unique=True, db_index=True)
    published = models.DateTimeField(_('Published'))
    image = models.ForeignKey(Photo, null=True, blank=True, related_name='news_images')

    is_public = models.BooleanField(_('Is public'), default=True)

    added = models.DateField(_('Added'), auto_now_add=True)
    modified = models.DateField(_('Modified'), auto_now=True)

    translations = TranslatedFields(
        title=models.CharField(_('Title'), max_length=200),
        summary=models.TextField(_('Summary'), blank=True),
        body=models.TextField(_('Body')),
    )

    def get_title(self):
        return self.title

    def get_absolute_url(self):
        return reverse('csnews_article', kwargs={'article_slug': self.slug})

    class Meta:
        verbose_name = _('Article')
        verbose_name_plural = _('Articles')
        ordering = ('-published',)
        get_latest_by = 'published'

    def __unicode__(self):
        return u'%s' % self.title
