from __future__ import unicode_literals

from rest_framework import serializers
from rest_framework.permissions import SAFE_METHODS

from nodeconductor.core.models import User
from nodeconductor.structure.models import Customer
from nodeconductor_organization import models


class OrganizationSerializer(serializers.HyperlinkedModelSerializer):

    customer = serializers.HyperlinkedRelatedField(
        view_name='customer-detail',
        lookup_field='uuid',
        queryset=Customer.objects.all(),
        allow_null=True
    )

    class Meta(object):
        model = models.Organization
        extra_kwargs = {
            'url': {'lookup_field': 'uuid'},
        }

    def validate(self, data):
        customer = data.get('customer')
        if customer is None:
            return super(OrganizationSerializer, self).validate(data)

        organizations = models.Organization.objects.filter(customer=customer)
        if organizations.exists():
            raise serializers.ValidationError('Organization for this customer already exist.')

        return super(OrganizationSerializer, self).validate(data)

    def get_fields(self):
        fields = super(OrganizationSerializer, self).get_fields()

        request = self.context['request']
        user = request.user

        if not user.is_staff:
            del fields['customer']

        return fields


class OrganizationUserSerializer(serializers.HyperlinkedModelSerializer):

    user = serializers.HyperlinkedRelatedField(
        view_name='user-detail',
        lookup_field='uuid',
        queryset=User.objects.all(),
    )
    username = serializers.ReadOnlyField(source='user.username')

    class Meta(object):
        model = models.OrganizationUser
        view_name = 'organization_user-detail'
        extra_kwargs = {
            'organization': {'lookup_field': 'uuid'},
            'url': {'lookup_field': 'uuid'},
        }

    def validate(self, data):
        user = data.get('user')
        organization_users = models.OrganizationUser.objects.filter(user=user)
        if organization_users.exists():
            raise serializers.ValidationError('User can belong only to one organization.')

        return super(OrganizationUserSerializer, self).validate(data)

    def get_fields(self):
        fields = super(OrganizationUserSerializer, self).get_fields()

        request = self.context['request']

        if not request.user.is_staff:
            fields['user'].queryset = User.objects.filter(uuid=request.user.uuid)

        if request.method not in SAFE_METHODS:
            del fields['is_approved']

        return fields
