from __future__ import unicode_literals

import django_filters

from nodeconductor.core import filters as core_filters
from nodeconductor.core.filters import UUIDFilter
from nodeconductor_organization import models


class OrganizationFilter(django_filters.FilterSet):
    customer_uuid = UUIDFilter(
        name='customer__uuid',
    )
    customer = core_filters.URLFilter(
        view_name='customer-detail',
        name='customer__uuid',
    )

    class Meta(object):
        model = models.Organization
        fields = [
            'name',
            'native_name',
            'abbreviation',
            'customer',
            'customer_uuid'
        ]
        order_by = [
            'name',
            'native_name',
            'abbreviation'
            # desc
            '-name',
            '-native_name',
            '-abbreviation'
        ]


class OrganizationUserFilter(django_filters.FilterSet):
    organization = core_filters.URLFilter(
        view_name='organization-detail',
        name='organization__uuid',
    )

    organization_uuid = UUIDFilter(
        name='organization__uuid',
    )

    user = core_filters.URLFilter(
        view_name='user-detail',
        name='user__uuid',
    )

    user_uuid = UUIDFilter(
        name='user__uuid',
    )

    class Meta(object):
        model = models.OrganizationUser
        fields = [
            'organization',
            'organization_uuid',
            'user',
            'user_uuid',
            'is_approved'
        ]
        order_by = [
            'is_approved',
            # desc
            '-is_approved'
        ]
