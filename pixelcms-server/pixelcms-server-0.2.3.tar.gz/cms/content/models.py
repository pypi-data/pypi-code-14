from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from autoslug import AutoSlugField
from filebrowser.fields import FileBrowseField

from cms.common import mixins, utils
from cms.common.fields import LanguageField, FilebrowserVersionField


HEADERS_LEVEL_CHOICES = (
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
    ('6', '6'),
)


class Category(mixins.Seo):
    name = models.CharField(_('name'), max_length=255)
    slug = AutoSlugField(
        _('slug'), populate_from='name', unique_with='parent',
        editable=True, blank=True
    )
    published = models.BooleanField(_('published'), default=True)
    order = models.PositiveSmallIntegerField(_('order'), default=0)
    language = LanguageField(_('language'))
    parent = models.ForeignKey(
        'self', verbose_name=_('parent'), related_name='_subcategories',
        null=True, blank=True
    )
    description = models.TextField(_('description'), blank=True, default='')

    show_description = models.BooleanField(
        _('show description'), default=True
    )
    show_article_intros = models.BooleanField(
        _('show article intros'), default=True
    )
    show_article_contents = models.BooleanField(
        _('show article contents'), default=False
    )
    show_articles_created = models.BooleanField(
        _('show article creation date'), default=False
    )
    show_article_images = models.BooleanField(
        _('show article images'),
        help_text=_('Shows thumbnail if set, otherwise first image.'),
        default=True
    )
    articles_images_size = FilebrowserVersionField(_('articles images size'))

    pagination = models.BooleanField(_('pagination'), default=True)
    articles_on_page = models.PositiveSmallIntegerField(
        _('articles on page'), default=10
    )

    show_breadcrumbs = models.BooleanField(
        _('show bradcrumbs'), default=True
    )
    show_back_link = models.BooleanField(_('show back link'), default=True)

    av_articles_images_thumbnails_size = FilebrowserVersionField(
        _('articles images size'), allow_null=True
    )

    class Meta:
        app_label = 'content'
        ordering = ('language',  'order', 'name')
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    def __str__(self):
        return self.name

    @property
    def route(self):
        if not self.published:
            return None

        def try_parents():
            tree = []
            parent = self.parent
            while(parent):
                current = parent
                if not current.published:
                    return None
                tree.append(current)
                parent = current.parent
            tree.reverse()
            tree.append(self)

            # root category must be published as page
            page = tree[0].pages.filter(published=True).first()
            if not page:
                return None

            if page.route == '/':
                path = ''
            else:
                path = page.route
            rest = '/'.join([c.slug for c in tree[1:]])
            if rest:
                path += '/{}'.format(rest)
            return path

        def try_page():
            page = self.pages.filter(published=True).first()
            if page:
                return page.route

        return try_parents() or try_page()

    @property
    def all_routes(self):
        if not self.published:
            return []
        routes = []
        if self.route:
            routes.append(self.route)
        for page in self.pages.filter(published=True):
            if page.route not in routes:
                routes.append(page.route)
        return routes

    @property
    def meta(self):
        return utils.generate_meta(
            title=self.meta_title_override or self.name,
            title_suffix=self.meta_title_site_name_suffix,
            description=self.meta_description_override,
            robots=self.meta_robots_override
        )

    @property
    def breadcrumbs(self):
        output = [{
            'name': self.name,
            'route': self.route
        }]
        parent = self.parent
        while parent:
            output.append({
                'name': parent.name,
                'route': parent.route
            })
            parent = parent.parent
        return reversed(output)

    @property
    def back_link(self):
        try:
            return self.parent.route
        except AttributeError:
            return '/'

    @property
    def subcategories(self):
        return self._subcategories.filter(
            published=True, language__in=utils.served_langs()
        )

    @property
    def articles(self):
        return self._articles.filter(
            published=True, language__in=utils.served_langs()
        )

    def get_article_image(self, article):
        try:
            image = article.thumbnail_or_first_image.original
        except AttributeError:
            return None
        version = self.articles_images_size
        return image.version_generate(version).url


class Article(mixins.Seo):
    title = models.CharField(_('title'), max_length=255)
    slug = AutoSlugField(
        _('slug'), populate_from='title', unique_with='category',
        editable=True, blank=True
    )
    published = models.BooleanField(_('published'), default=True)
    order = models.PositiveSmallIntegerField(_('order'), default=0)
    language = LanguageField(_('language'))
    category = models.ForeignKey(
        Category, verbose_name=_('category'), related_name='_articles',
        null=True, blank=True
    )
    thumbnail = FileBrowseField(
        _('thumbnail'), help_text=_('Displayed in category view.'),
        format='Image', max_length=255, null=True, blank=True
    )
    intro = models.TextField(_('intro'), blank=True, default='')
    content = models.TextField(_('content'), blank=True, default='')

    show_created = models.BooleanField(_('show creation date'), default=False)
    show_breadcrumbs = models.BooleanField(_('show breadcrumbs'), default=True)
    show_back_link = models.BooleanField(_('show back link'), default=True)
    images_thumbnails_size = FilebrowserVersionField(
        _('images thumbnails size'), allow_null=True
    )

    created = models.DateTimeField(_('creation date'), default=timezone.now)
    last_modified = models.DateTimeField(
        _('last modification date'), auto_now=True
    )

    class Meta:
        app_label = 'content'
        ordering = ('language', 'category', 'order', 'title')
        verbose_name = _('article')
        verbose_name_plural = _('articles')

    def __str__(self):
        return self.title

    @property
    def route(self):
        if not self.published:
            return None
        category = self.category
        if category:
            if category.route:
                if category.route == '/':
                    category_route = ''
                else:
                    category_route = category.route
                return '{}/{}'.format(category_route, self.slug)
        page = self.pages.filter(published=True).first()
        if page:
            return page.route
        return None

    @property
    def all_routes(self):
        if not self.published:
            return []
        routes = []
        if self.route:
            routes.append(self.route)
        for page in self.pages.filter(published=True):
            if page.route not in routes:
                routes.append(page.route)
        return routes

    @property
    def meta(self):
        return utils.generate_meta(
            title=self.meta_title_override or self.title,
            title_suffix=self.meta_title_site_name_suffix,
            description=self.meta_description_override,
            robots=self.meta_robots_override
        )

    @property
    def breadcrumbs(self):
        output = [{
            'name': self.title,
            'route': self.route
        }]
        parent = self.category
        while parent:
            if parent.route:
                output.append({
                    'name': parent.name,
                    'route': parent.route
                })
            parent = parent.parent
        return reversed(output)

    @property
    def back_link(self):
        try:
            return self.category.route or '/'
        except AttributeError:
            return '/'

    @property
    def thumbnail_or_first_image(self):
        try:
            return self.thumbnail or self.images.filter(published=True) \
                .first().image
        except AttributeError:
            return None


class ArticleImage(models.Model):
    article = models.ForeignKey(
        Article, verbose_name=_('article'), related_name='images'
    )
    image = FileBrowseField(
        _('image'), format='Image',
        max_length=200, null=True, blank=True
    )
    published = models.BooleanField(_('published'), default=True)
    order = models.PositiveSmallIntegerField(_('order'), default=0)
    title = models.CharField(
        _('title'), max_length=255, blank=True, default=''
    )

    class Meta:
        app_label = 'content'
        ordering = ('order',)
        verbose_name = _('image')
        verbose_name_plural = _('images')

    def get_thumbnail(self):
        try:
            version = (
                self.article.images_thumbnails_size or
                self.article.category.av_articles_images_thumbnails_size or
                '3cols'
            )
        except AttributeError:
            version = '3cols'

        return self.image.original.version_generate(version).url


class ContentModule(mixins.Module):
    content = models.TextField(_('content'))

    class Meta(mixins.Module.Meta):
        app_label = 'content'
        verbose_name = _('content module')
        verbose_name_plural = _('content modules')


class ArticlesModule(mixins.Module):
    articles = models.ManyToManyField(
        Article, through='ArticlesModuleArticle', blank=True
    )
    categories = models.ManyToManyField(
        Category, through='ArticlesModuleCategory', blank=True
    )

    articles_limit = models.SmallIntegerField(_('articles limit'), default=5)
    show_articles_titles = models.BooleanField(
        _('show articles titles'), default=True
    )
    articles_titles_headers_level = models.CharField(
        _('articles titles headers level'), max_length=1,
        choices=HEADERS_LEVEL_CHOICES, default='3'
    )
    show_article_images = models.BooleanField(
        _('show article images'), default=True
    )
    articles_images_size = FilebrowserVersionField(_('articles images size'))
    show_articles_intros = models.BooleanField(
        _('show articles intros'), default=True
    )
    show_articles_contents = models.BooleanField(
        _('show articles contents'), default=True
    )

    class Meta(mixins.Module.Meta):
        app_label = 'content'
        verbose_name = _('articles module')
        verbose_name_plural = _('articles modules')

    @property
    def items(self):
        articles_pks = self.articles.filter(
            published=True, language__in=utils.served_langs()
        ).values_list('pk', flat=True)

        categories = self.categories.filter(
            published=True, language__in=utils.served_langs()
        )
        articles_from_categories_pks = Article.objects.filter(
            published=True, language__in=utils.served_langs(),
            category__in=categories
        ).values_list('pk', flat=True)

        pks = list(articles_pks) + list(articles_from_categories_pks)

        articles = Article.objects.filter(pk__in=pks)[:self.articles_limit]
        return articles

    def get_article_image(self, article):
        try:
            image = article.thumbnail_or_first_image.original
        except AttributeError:
            return None
        version = self.articles_images_size
        return image.version_generate(version).url


class ArticlesModuleArticle(models.Model):
    module = models.ForeignKey(ArticlesModule)
    article = models.ForeignKey(Article)
    order = models.PositiveSmallIntegerField(_('order'), default=0)

    class Meta:
        app_label = 'content'
        ordering = ('order',)
        verbose_name = _('article')
        verbose_name_plural = _('articles')

    def __str__(self):
        return self.article.title


class ArticlesModuleCategory(models.Model):
    module = models.ForeignKey(ArticlesModule)
    category = models.ForeignKey(Category)
    order = models.PositiveSmallIntegerField(_('order'), default=0)

    class Meta:
        app_label = 'content'
        ordering = ('order',)
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    def __str__(self):
        return self.category.name
