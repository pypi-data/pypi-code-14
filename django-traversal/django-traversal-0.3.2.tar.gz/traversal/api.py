# coding: utf-8
from django.shortcuts import redirect
from django.http import HttpResponse
from decorators import respounse_or_redirect
from router import api_route_factory
from templatetags.traversal_url import turl_replace, turl_sub_all, turl_add_hierarchy, turl_add, turl_replace_all, turl_sub


"""
АПИ для работы с traversal-url из JS
"""


def get_context(request):
    """
    Принимает url и находит по нему контекст
    :return: context
    """
    url = request.GET['url']
    return api_route_factory(request, url)


@respounse_or_redirect()
def turl_replace_api(request, str_res_class_name_or_array, res_slug_or_slugs):
    res_slug_or_slugs = res_slug_or_slugs.split('.')
    return turl_replace(get_context(request), str_res_class_name_or_array, *res_slug_or_slugs)


@respounse_or_redirect()
def turl_replace_all_api(request, str_res_class_name_or_array, str_no_replace_res_class_name_or_array, res_slug_or_slugs):
    res_slug_or_slugs = res_slug_or_slugs.split('.')
    return turl_replace_all(get_context(request), str_res_class_name_or_array, str_no_replace_res_class_name_or_array, *res_slug_or_slugs)


@respounse_or_redirect()
def turl_sub_api(request, str_res_class_name_or_array, res_slug_or_slugs):
    res_slug_or_slugs = res_slug_or_slugs.split('.')
    return turl_sub(get_context(request), str_res_class_name_or_array, *res_slug_or_slugs)


@respounse_or_redirect()
def turl_sub_all_api(request, str_res_class_name_or_array):
    return turl_sub_all(get_context(request), str_res_class_name_or_array)


@respounse_or_redirect()
def turl_add_hierarchy_api(request, hierarchy_parent_slug, str_res_class_name_or_array, res_slug_or_slugs):
    res_slug_or_slugs = res_slug_or_slugs.split('.')
    return turl_add_hierarchy(get_context(request), hierarchy_parent_slug, str_res_class_name_or_array, *res_slug_or_slugs)


@respounse_or_redirect()
def turl_add_api(request, str_res_class_name_or_array, res_slug_or_slugs):
    res_slug_or_slugs = res_slug_or_slugs.split('.')
    return turl_add(get_context(request), str_res_class_name_or_array, *res_slug_or_slugs)