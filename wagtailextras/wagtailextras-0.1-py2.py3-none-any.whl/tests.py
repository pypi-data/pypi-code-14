from wagtail.tests.utils import WagtailPageTests
from wagtail.wagtailcore.models import Page

from wagtailextras.mixins import UniquePageMixin

class UniquePageMixinPage(UniquePageMixin, Page):
    pass

class MyPageTests(WagtailPageTests):
    def test_can_create_a_page(self):
        UniquePageMixin.objects.create()
