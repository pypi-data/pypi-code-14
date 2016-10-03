from django.conf.urls import url

from traversal.router import route_factory
from api import turl_replace_api, turl_sub_all_api, turl_replace_all_api, turl_sub_api, turl_add_api, turl_add_hierarchy_api

urlpatterns = [
    # api
    url(r'^tapi/turl_add_hierarchy/(?P<str_res_class_name_or_array>[\.A-Za-z0-9_-]+)/(?P<res_slug_or_slugs>[\/\w \:\.\,\+-]+)', turl_add_hierarchy_api, name='turl_add_hierarchy_api'),
    url(r'^tapi/turl_add/(?P<str_res_class_name_or_array>[\.A-Za-z0-9_-]+)/(?P<res_slug_or_slugs>[\/\w \:\.\,\+-]+)', turl_add_api, name='turl_add_api'),
    url(r'^tapi/turl_sub/(?P<str_res_class_name_or_array>[\.A-Za-z0-9_-]+)/(?P<res_slug_or_slugs>[\/\w \:\.\,\+-]+)', turl_sub_api, name='turl_sub_api'),
    url(r'^tapi/turl_replace_all/(?P<str_res_class_name_or_array>[\.A-Za-z0-9_-]+)/(?P<res_slug_or_slugs>[\/\w \:\.\,\+-]+)', turl_replace_all_api, name='turl_replace_all_api'),
    url(r'^tapi/turl_replace/(?P<str_res_class_name_or_array>[\.A-Za-z0-9_-]+)/(?P<res_slug_or_slugs>[\/\w \:\.\,\+-]+)', turl_replace_api, name='turl_replace_api'),
    url(r'^tapi/turl_sub_all/(?P<str_res_class_name_or_array>[\.A-Za-z0-9_-]+)', turl_sub_all_api, name='turl_sub_all_api'),

    # router
    url(r'^(\S+)', route_factory, name='router'),
    url(r'^', route_factory, name='router_root'),
]
