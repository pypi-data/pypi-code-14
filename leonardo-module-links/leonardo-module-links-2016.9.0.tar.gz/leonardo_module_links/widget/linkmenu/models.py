# -#- coding: utf-8 -#-

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from leonardo.module.web.models import ListWidget

from leonardo_module_links.models import LinkCategory
from .forms import LinksWidgetForm


class LinkMenuWidget(ListWidget):

    feincms_item_editor_form = LinksWidgetForm

    list = models.ForeignKey(LinkCategory, verbose_name=_(
        "link category"), related_name="%(app_label)s_%(class)s_related")

    def get_items(self, **kwargs):
        return self.list.link_set.filter(visible=True).order_by('ordering')

    def thumb_geom(self):
        return getattr(settings,
                       'MEDIA_THUMB_MEDIUM_GEOM',
                       '96x96')

    class Meta:
        abstract = True
        verbose_name = _("links menu")
        verbose_name_plural = _('links menus')
