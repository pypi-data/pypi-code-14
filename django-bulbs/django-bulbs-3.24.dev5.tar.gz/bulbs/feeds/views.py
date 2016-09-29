from collections import OrderedDict
from elasticsearch_dsl.filter import Not, Type, Term
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from django.template import RequestContext
from django.utils.timezone import now

from bulbs.content.filters import Published
from bulbs.content.models import Content
from bulbs.content.views import ContentListView
from bulbs.special_coverage.models import SpecialCoverage
from bulbs.super_features.utils import get_superfeature_model

from .serializers import GlanceContentSerializer


class RSSView(ContentListView):
    """Really simply, this syndicates Content."""
    template_name = "feeds/rss.xml"
    paginate_by = 20
    feed_title = "RSS Feed"
    utm_params = "utm_medium=RSS&amp;utm_campaign=feeds"

    def get_template_names(self):
        return ["feeds/rss.xml", "feeds/_rss.xml"]

    def get(self, request, *args, **kwargs):
        response = super(RSSView, self).get(request, *args, **kwargs)
        response["Content-Type"] = "application/rss+xml"
        return response

    def get_queryset(self):
        return super(RSSView, self).get_queryset().filter(
            # Exclude all SuperFeatures (until we ever decide to support them)
            Not(filter=Type(value=get_superfeature_model().search_objects.mapping.doc_type))
        ).filter(
            Term(**{'hide_from_rss': False})
        )

    def get_context_data(self, *args, **kwargs):
        context = super(RSSView, self).get_context_data(*args, **kwargs)
        context["full"] = (self.request.GET.get("full", "false").lower() == "true")
        context["images"] = (self.request.GET.get("images", "false").lower() == "true")
        context["build_date"] = now()
        context["title"] = self.feed_title
        context["feed_url"] = self.request.build_absolute_uri()
        context["search_url"] = self.request.build_absolute_uri(
            u"/search?%s" % self.request.META["QUERY_STRING"])

        # OK, so this is kinda brutal. Stay with me here.
        for content in context["page_obj"].object_list:
            feed_path = content.get_absolute_url() + "?" + self.utm_params
            content.feed_url = self.request.build_absolute_uri(feed_path)

        return RequestContext(self.request, context)


class SpecialCoverageRSSView(RSSView):
    """Really simply, this syndicates Content."""
    feed_title = "Special Coverage RSS Feed"

    def get_queryset(self):
        sc_id = self.request.GET.get("special_coverage_id")
        sc_slug = self.request.GET.get("special_coverage_slug")

        if sc_id:
            sc = SpecialCoverage.objects.get(id=sc_id)
        elif sc_slug:
            sc = SpecialCoverage.objects.get(slug=sc_slug)
        else:
            return self.model.objects.none()

        return sc.get_content()[:self.paginate_by]


class GlanceFeedViewSet(viewsets.ReadOnlyModelViewSet):

    model = Content
    serializer_class = GlanceContentSerializer

    queryset = Content.search_objects.search().sort('-last_modified').filter(Published())

    permission_classes = (AllowAny,)

    class GlancePageNumberPagination(PageNumberPagination):
        page_size = 20
        page_size_query_param = 'per_page'
        max_page_size = 100   # Section percolator calls can be expensive

        # Customized for Glance's format
        def get_paginated_response(self, data):
            pagination = OrderedDict([
                ('page', self.page.number),    # TODO: Correct?
                ('per_page', self.page.paginator.per_page),
                ('total', self.page.paginator.count),
                ('content', data)
            ])

            # Per spec, only include 'next' if valid
            if self.get_next_link():
                pagination['next'] = self.get_next_link()

            return Response(pagination)

        def _handle_backwards_compat(self, view):
            # Override parent method to do nothing :)
            # Avoid any deprecated PAGINATION values from property `settings` files.
            # Sites like Onion set 'PAGINATE_BY_PARAM' to 'page_size', which overrrides this class's custom
            # 'per_page' param name.
            # Necessary for DRF v3.1, but won't need this override for DRF v3.3+
            pass

    pagination_class = GlancePageNumberPagination
