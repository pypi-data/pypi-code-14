from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.conf import settings
from django.http import Http404
from .models import Interview, Product
from .managers import published


class InterviewDetailView(DetailView):
    def get_queryset(self):
        queryset = Interview.objects.published()
        return queryset

    def get_context_data(self, **kwargs):
        context = super(InterviewDetailView, self).get_context_data(**kwargs)
        context['pictures'] = self.object.interviewpicture_set.all()
        context['latest_interviews'] = Interview.objects.published().exclude(slug__exact=self.kwargs['slug'])[:2]
        return context


class PreviewInterviewDetailView(DetailView):
    def get_object(self):
        obj = Interview.objects.on_site().get(slug=self.kwargs['slug'])
        if obj.preview_hash == self.kwargs.get('hash', ""):
            return obj
        else:
            raise Http404

    def get_context_data(self, **kwargs):
        context = super(PreviewInterviewDetailView, self).get_context_data(**kwargs)
        context['pictures'] = self.object.interviewpicture_set.all()
        context['latest_interviews'] = Interview.objects.published().exclude(slug__exact=self.kwargs['slug'])[:2]
        context['is_preview'] = True
        return context


class InterviewListView(ListView):
    paginate_by = 10

    def get_queryset(self):
        queryset = Interview.objects.published()
        if 'filter_key' in self.kwargs:
            if self.kwargs['filter_key'] in ['sexe']:
                if self.kwargs['filter_value'] == 'homme':
                    queryset = queryset.filter(person__sex=1)
                elif self.kwargs['filter_value'] == 'femme':
                    queryset = queryset.filter(person__sex=2)
                else:
                    raise Http404()
            else:
                raise Http404()
        return queryset

    def get_current_filter(self):
        current_filter = None
        queryset = self.get_queryset()
        if 'filter_key' in self.kwargs:
            if self.kwargs['filter_key'] in ['sexe']:
                if self.kwargs['filter_value'] == 'homme':
                    queryset = queryset.filter(person__sex=1)
                    current_filter = 'sexe'
                elif self.kwargs['filter_value'] == 'femme':
                    queryset = queryset.filter(person__sex=2)
                    current_filter = 'sexe'
        return current_filter

    def get_context_data(self, **kwargs):
        context = super(InterviewListView, self).get_context_data(**kwargs)
        context['filter'] = self.get_current_filter()
        context['filter_key'] = self.kwargs.get('filter_key', None)
        context['filter_value'] = self.kwargs.get('filter_value', None)
        context['total_interviews'] = Interview.objects.published().count()
        return context


class ProductDetailView(DetailView):
    def get_object(self):
        obj = super(ProductDetailView, self).get_object()
        if not obj.is_online:
            if not (self.request.user.is_authenticated() and self.request.user.is_staff):
                raise Http404
        return obj

    def get_queryset(self):
        queryset = Product.objects.all()
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context['interviews'] = Interview.objects.published().filter(products__product=self.object)
        return context


class ProductListView(ListView):
    paginate_by = 12

    def get_queryset(self):
        if not (self.request.user.is_authenticated() and self.request.user.is_staff):
            raise Http404
        queryset = Product.objects.all()
        return queryset
