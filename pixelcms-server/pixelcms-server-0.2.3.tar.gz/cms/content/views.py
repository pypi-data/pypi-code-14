from django.shortcuts import get_object_or_404

from rest_framework import generics

from cms.common.utils import current_lang, served_langs
from .models import Category, ContentModule, ArticlesModule
from .serializers import CategorySerializer, ContentModuleSerializer, \
    ArticlesModuleSerializer


class CategoryView(generics.RetrieveAPIView):
    queryset = Category.objects.filter(published=True)
    serializer_class = CategorySerializer


class ContentModuleView(generics.RetrieveAPIView):
    queryset = ContentModule.objects.filter(published=True)
    serializer_class = ContentModuleSerializer
    lookup_field = 'template_id'

    def get_object(self):
        queryset = self.get_queryset()
        filters = {}
        filters[self.lookup_field] = self.kwargs[self.lookup_field]
        try:
            filters['language'] = current_lang()
            obj = queryset.get(**filters)
        except ContentModule.DoesNotExist:
            del filters['language']
            filters['language__in'] = served_langs()
            obj = get_object_or_404(queryset, **filters)
        return obj


class ArticlesModuleView(generics.RetrieveAPIView):
    queryset = ArticlesModule.objects.filter(published=True)
    serializer_class = ArticlesModuleSerializer
    lookup_field = 'template_id'

    def get_object(self):
        queryset = self.get_queryset()
        filters = {}
        filters[self.lookup_field] = self.kwargs[self.lookup_field]
        try:
            filters['language'] = current_lang()
            obj = queryset.get(**filters)
        except ArticlesModule.DoesNotExist:
            del filters['language']
            filters['language__in'] = served_langs()
            obj = get_object_or_404(queryset, **filters)
        return obj
