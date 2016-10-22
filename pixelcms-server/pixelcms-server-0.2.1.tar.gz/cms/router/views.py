from django.shortcuts import Http404

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from cms.common.utils import served_langs
from cms.pages.models import Page, PageCategory
from cms.content.models import Category, Article
from cms.content.serializers import ArticleSerializer, CategorySerializer


@api_view()
def pageView(request, slug, homepage=False):
    if homepage:
        try:
            page = Page.objects.get(
                homepage=True, published=True, language__in=served_langs()
            )
            return page.get_view(request)
        except Page.DoesNotExist:
            raise Http404

    try:
        page = Page.objects.get(
            homepage=False, slug=slug,
            published=True, language__in=served_langs()
        )
        return page.get_view(request)
    except Page.DoesNotExist:
        raise Http404


# routes to category descendant (subcategory or article)
@api_view()
def contentView(request, path):
    path = path.split('/')
    try:
        # first slice of path must be PageCategory
        root_category_page = Page.objects \
            .instance_of(PageCategory) \
            .get(slug=path[0], published=True, language__in=served_langs())
        if root_category_page.deps_published is False:
            raise Http404
    except Page.DoesNotExist:
        raise Http404

    remaining_path = path[1:]
    parent = root_category_page.category
    for i, slug in enumerate(remaining_path):
        if i == len(remaining_path) - 1:
            # last slice can be Article or Category
            try:
                category = Category.objects.get(
                    slug=slug, published=True, parent=parent,
                    language__in=served_langs()
                )
                return Response({
                    'component_name': 'Category',
                    'component_data': CategorySerializer(category).data,
                    'meta': category.meta
                })
            except Category.DoesNotExist:
                pass
            try:
                article = Article.objects.get(
                    slug=slug, published=True, category=parent,
                    language__in=served_langs()
                )
                return Response({
                    'component_name': 'Article',
                    'component_data': ArticleSerializer(article).data,
                    'meta': article.meta
                })
            except Article.DoesNotExist:
                raise Http404
        else:
            # not-last slice must be Category
            try:
                category = Category.objects.get(
                    slug=slug, published=True, parent=parent,
                    language__in=served_langs()
                )
                parent = category
            except Category.DoesNotExist:
                raise Http404
