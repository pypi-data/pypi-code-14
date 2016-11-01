from django.contrib.sites.models import Site
from django.db import models

class PiwikConfiguration(models.Model):
    site = models.OneToOneField(Site, related_name='piwik_configuration')

    piwik_url = models.URLField(default='')
    piwik_site_id = models.PositiveSmallIntegerField()
    piwik_token_auth = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return "%s (%s): ID %s" % (self.site.domain, self.site.name, self.piwik_site_id)
