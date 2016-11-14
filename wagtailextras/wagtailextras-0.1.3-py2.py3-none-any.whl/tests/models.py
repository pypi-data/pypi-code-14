from wagtail.wagtailcore.models import Page

from wagtailextras.mixins import UniquePageMixin


class UniquePageMixinPage(UniquePageMixin, Page):
    pass