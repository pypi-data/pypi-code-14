from wagtail.tests.utils import WagtailPageTests

from wagtail.wagtailcore.models import Page

from build.lib.wagtailextras.blocks import EmptyBlock
from wagtailextras.tests.models import UniquePageMixinPage


class MyPageTests(WagtailPageTests):
    def setUp(self):
        pass

    def test_can_create_a_page(self):
        # x = UniquePageMixinPage.objects.create()
        self.assertCanCreateAt(UniquePageMixinPage, Page)
        print(EmptyBlock)
