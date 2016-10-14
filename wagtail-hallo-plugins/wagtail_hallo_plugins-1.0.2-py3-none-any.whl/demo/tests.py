from wagtail.tests.utils import WagtailPageTests
from wagtail.wagtailcore.models import Page
from .models import DemoPage


class PluginsTest(WagtailPageTests):
    """ Very basic tests to ensure plugins don't cause errors
    This won't catch javascript issues.
    """
    def test_page_with_richtext(self):
        """ Create demo_page with rich text and load the edit view """
        root_page = Page.objects.first()
        demo_page = DemoPage(title="demo", slug="demo", body="body")
        root_page.add_child(instance=demo_page)
        url = '/admin/pages/{}/edit/'.format(demo_page.id)
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
