from django.contrib.sitemaps import Sitemap
from .models import Interview


class InterviewSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return Interview.objects.published()

    def lastmod(self, obj):
        return obj.updated_on
