from wagtail.tests.utils import WagtailPageTests
from django.test import TestCase

from wagtail.wagtailcore.models import Page

from build.lib.wagtailextras.blocks import EmptyBlock
from wagtailextras.mixins import UniquePageMixin

# class UniquePageMixinPage(UniquePageMixin, Page):
#     pass

class MyPageTests(WagtailPageTests):
    def test_can_create_a_page(self):
        print(EmptyBlock)


        # UniquePageMixin.objects.create()
