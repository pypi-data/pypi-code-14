from __future__ import unicode_literals

from nodeconductor_organization import views


def register_in(router):
    router.register(r'organizations', views.OrganizationViewSet, base_name='organization')
    router.register(r'organization-users', views.OrganizationUserViewSet, base_name='organization_user')
