from django.conf import settings
from django.utils.html import format_html


class Icon(object):

    def __init__(self, id):
        self.id = id

    def as_html(self):
        if not self.id:
            return ''

        prefix = 'juta-portfolio-iconjuta-portfolio-icon-'
        return format_html('<span class="juta-portfolio-icon-{0}"></span>', prefix, self.id)

    def __str__(self):
        return self.id

    def __unicode__(self):
        return str(self)