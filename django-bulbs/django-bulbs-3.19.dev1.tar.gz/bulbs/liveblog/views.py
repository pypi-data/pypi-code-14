from django.conf import settings
from django.db.models.loading import get_model
from django.http import Http404
from django.utils import timezone
from django.views.decorators.cache import cache_control

from bulbs.content.views import BaseContentDetailView

LiveBlogModel = get_model(settings.LIVEBLOG_MODEL)


def entries_page(liveblog, cursor_entry=None):
    entries_query = liveblog.entries.order_by('-published')
    if cursor_entry:
        entries_query = entries_query.filter(
            published__isnull=False,
            published__lte=timezone.now(),
            published__lt=cursor_entry.published)
    else:
        entries_query = entries_query.filter(
            published__lte=timezone.now())
    return entries_query[:10]


class LiveBlogDetailViewMixin(object):

    def get_context_data(self, *args, **kwargs):
        context = super(LiveBlogDetailViewMixin, self).get_context_data(*args, **kwargs)
        context['entries'] = entries_page(liveblog=self.object)
        return context


class LiveBlogMoreEntriesView(BaseContentDetailView):
    model = LiveBlogModel
    template_name = 'liveblog/more_entries.html'
    redirect_correct_path = False

    def get_context_data(self, object):
        context = {}
        cursor_entry = object.entries.filter(
            published__lte=timezone.now,
            pk=self.kwargs['cursor_entry']).first()
        if cursor_entry is None:
            raise Http404()
        context['content'] = self.object
        context['entries'] = entries_page(liveblog=self.object, cursor_entry=cursor_entry)
        return context


class LiveBlogNewEntriesView(BaseContentDetailView):
    model = LiveBlogModel
    template_name = 'liveblog/new_entries.html'
    redirect_correct_path = False

    def get_context_data(self, object):
        context = {}
        if 'entry_ids' not in self.request.GET:
            raise ValueError('param "entry_ids" MUST be specified')
        parsed_entry_ids = [x.strip() for x in self.request.GET['entry_ids'].split(',')]
        context['entries'] = self.object.entries.filter(
            pk__in=parsed_entry_ids,
            published__lte=timezone.now())
        return context

liveblog_more_entries = cache_control(max_age=600)(LiveBlogMoreEntriesView.as_view())
liveblog_new_entries = cache_control(max_age=600)(LiveBlogNewEntriesView.as_view())
