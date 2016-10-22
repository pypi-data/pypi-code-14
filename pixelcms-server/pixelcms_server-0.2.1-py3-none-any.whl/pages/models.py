from django.db import models
from django.utils.translation import ugettext_lazy as _

from polymorphic.models import PolymorphicModel
from autoslug import AutoSlugField
from rest_framework.response import Response
from rest_framework import status

from cms.common import mixins, utils
from cms.common.fields import LanguageField
from cms.content.models import Category, Article
from cms.content.serializers import CategorySerializer, ArticleSerializer


class Page(PolymorphicModel):
    title = models.CharField(_('title'), max_length=255)
    slug = AutoSlugField(
        _('slug'), populate_from='title', unique_with='language',
        editable=True, blank=True
    )
    published = models.BooleanField(_('published'), default=True)
    order = models.PositiveSmallIntegerField(_('order'), default=0)

    homepage = models.BooleanField(_('homepage'), default=False)

    react_component_name = models.CharField(
        _('react component name'), help_text=_('Leave it blank to use default '
                                               'component.'),
        max_length=255, null=True, blank=True
    )

    language = LanguageField(_('language'))

    class Meta:
        app_label = 'pages'
        ordering = ('language', 'order', 'title')
        verbose_name = _('page')
        verbose_name_plural = _('pages')

    def __str__(self):
        return self.title

    @property
    def route(self):
        if not self.pk:
            return ''
        if self.homepage:
            return '/'
        return '/{}'.format(self.slug)

    @property
    def deps_published(self):
        return True

    def get_meta(self):
        return utils.generate_meta(
            title=self.meta_title_override or self.title,
            title_suffix=self.meta_title_site_name_suffix,
            description=self.meta_description_override,
            robots=self.meta_robots_override
        )

    def get_view(self, request):
        if not self.deps_published:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response({
            'component_name': (
                self.react_component_name or self.DEFAULT_REACT_COMPONENT_NAME
            ),
            'component_data': self.get_component_data(request),
            'meta': self.get_meta()
        })


class PageCategory(Page):
    DEFAULT_REACT_COMPONENT_NAME = 'Category'

    category = models.ForeignKey(
        Category, verbose_name=_('category'), related_name='pages'
    )

    class Meta:
        app_label = 'pages'
        verbose_name = _('category page')
        verbose_name_plural = _('category pages')

    @property
    def deps_published(self):
        return self.category.published

    def get_component_data(self, request):
        return CategorySerializer(
            self.category, context={'request': request}
        ).data

    def get_meta(self):
        return self.category.meta


class PageArticle(Page):
    DEFAULT_REACT_COMPONENT_NAME = 'Article'

    article = models.ForeignKey(
        Article, verbose_name=_('article'), related_name='pages'
    )

    class Meta:
        app_label = 'pages'
        verbose_name = _('article page')
        verbose_name_plural = _('article pages')

    @property
    def deps_published(self):
        return self.article.published

    def get_component_data(self, request):
        return ArticleSerializer(
            self.article, context={'request': request}
        ).data

    def get_meta(self):
        return self.article.meta


class PageCustomComponent(Page, mixins.Seo):
    DEFAULT_REACT_COMPONENT_NAME = ''

    class Meta:
        app_label = 'pages'
        verbose_name = _('custom component page')
        verbose_name_plural = _('custom component pages')

    def get_component_data(self, request):
        return {}
