from __future__ import absolute_import, unicode_literals

from django.utils.functional import cached_property
from wagtail.wagtailcore.blocks import ChooserBlock


class NewsChooserBlock(ChooserBlock):
    def __init__(self, target_model, **kwargs):
        super(NewsChooserBlock, self).__init__(**kwargs)
        self.target_model = target_model

    @cached_property
    def widget(self):
        from wagtailnews.widgets import AdminNewsChooser
        return AdminNewsChooser(self.target_model)

    class Meta:
        icon = "grip"
