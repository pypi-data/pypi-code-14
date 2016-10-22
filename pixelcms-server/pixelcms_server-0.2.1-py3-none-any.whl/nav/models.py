from django.db import models
from django.utils.translation import ugettext_lazy as _

from cms.common import mixins
from cms.pages.models import Page


class NavModule(mixins.Module):
    class Meta(mixins.Module.Meta):
        app_label = 'nav'
        verbose_name = _('nav module')
        verbose_name_plural = _('nav modules')

    def __str__(self):
        return self.name

    def get_items(self):
        return self.items.filter(published=True)


class NavModuleItem(models.Model):
    nav = models.ForeignKey(
        NavModule, verbose_name=_('nav'), related_name='items'
    )
    name = models.CharField(
        _('name'), help_text=_('Overrides <strong>Page</strong> title. '
                               'Required when nav scrolls to element or is '
                               'link.'),
        max_length=255, null=True, blank=True
    )
    page = models.ForeignKey(
        Page, verbose_name=_('page'),
        null=True, blank=True
    )
    scroll_to_element = models.CharField(
        _('scroll to element'), help_text=_('HTML id of element on page. '
                                            'Overrides <strong>Page'
                                            '</strong>.'),
        max_length=255, blank=True, default=''
    )
    link = models.CharField(
        _('link'), help_text=_('Overrides <strong>Page</strong> and <strong>'
                               'Scroll to element</strong>.'),
        max_length=255, blank=True, default=''
    )
    link_open_in_new_tab = models.BooleanField(
        _('open link in new tab'), default=False
    )
    published = models.BooleanField(_('published'), default=True)
    order = models.PositiveSmallIntegerField(_('order'), default=0)

    class Meta:
        app_label = 'nav'
        ordering = ('order',)
        verbose_name = _('item')
        verbose_name_plural = _('items')

    def __str__(self):
        return self.get_name()

    @property
    def route(self):
        try:
            return self.page.route
        except AttributeError:
            return None

    def get_name(self):
        return self.name or self.page.title
