# -*- coding: utf-8
from __future__ import unicode_literals

from django.conf import settings
from django.http import Http404
from django.http import HttpResponse
from django.views.generic import TemplateView


class ACMEChallengeView(TemplateView):
    def get(self, request, *args, **kwargs):
        if settings.ACME_CHALLENGE_URL_SLUG and settings.ACME_CHALLENGE_TEMPLATE_CONTENT:
            if self.kwargs['challenge_slug'] == settings.ACME_CHALLENGE_URL_SLUG:
                return HttpResponse(settings.ACME_CHALLENGE_TEMPLATE_CONTENT)
        raise Http404("Invalid ACME challenge config")
