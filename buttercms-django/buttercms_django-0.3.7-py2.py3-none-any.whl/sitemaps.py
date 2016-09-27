from django.contrib import sitemaps
from django.core.urlresolvers import reverse

from . import api


class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        butter = api.ButterCms()
        response = butter.get_sitemap()
        return response

    def location(self, item):
        return reverse('blog_post', args=[item['slug']])