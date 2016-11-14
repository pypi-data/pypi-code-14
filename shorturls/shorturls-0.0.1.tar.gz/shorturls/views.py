# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.http import (
    JsonResponse, HttpResponse, HttpResponseBadRequest, HttpResponseRedirect)
from django.utils.translation import ugettext as _, force_text
from django.views.generic import View
from django.views.generic.detail import BaseDetailView

from .models import Url

url_validator = URLValidator()


class RegisterUrlView(View):
    """
    This is a simple AJAX view that returns an unused short URL for a given
    absolute URL.
    """
    http_method_names = ['get', 'post', 'options']

    def get(self, request, *args, **kwargs):
        url = request.POST.get('url', request.GET.get('url', None))
        try:
            url_validator(url)
        except ValidationError:
            return HttpResponseBadRequest(
                content=_('Please provide a valid URL to register.'))

        url_obj, __ = Url.objects.get_or_create(url=url)
        current_site = get_current_site(request)
        absolute_url = '{protocol}://{host}{url}'.format(
            protocol=getattr(settings, 'SHORTURLS_PROTOCOOL', 'http'),
            host=current_site.domain,
            url=url_obj.get_short_url()
        )
        if request.is_ajax():
            return JsonResponse({'url': absolute_url})
        else:
            # TODO: Template this?
            return HttpResponse(content=absolute_url)

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)  # pragma: no cover


class BaseShortUrlView(BaseDetailView):
    http_method_names = ['get', ]
    slug_field = 'code'
    slug_url_kwarg = 'code'
    model = Url


class RedirectShortUrlView(BaseShortUrlView):
    """
    This will simply redirect to the absolute URL for the given shorturl.
    """
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return HttpResponseRedirect(self.object.get_absolute_url(), status=302)


class ShortUrlMetricsView(BaseShortUrlView):
    def get_context_data(self, **kwargs):
        return {
            'counter': self.object.counter
        }

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        if request.is_ajax():
            return JsonResponse(self.get_context_data())
        else:
            # TODO: This should be a TemplateView of some sort
            return HttpResponse(content=force_text(self.get_context_data()))
