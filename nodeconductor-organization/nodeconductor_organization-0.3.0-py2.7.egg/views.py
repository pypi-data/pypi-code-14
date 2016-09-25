from __future__ import unicode_literals

from django.db.models import Q
from rest_framework import filters as rf_filters
from rest_framework import mixins
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from nodeconductor.core.permissions import IsAdminOrReadOnly
from nodeconductor.structure.models import CustomerRole
from nodeconductor_organization import filters
from nodeconductor_organization import models
from nodeconductor_organization import permissions
from nodeconductor_organization import serializers


class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = models.Organization.objects.all()
    serializer_class = serializers.OrganizationSerializer
    permission_classes = (IsAuthenticated, IsAdminOrReadOnly)
    filter_backends = (rf_filters.DjangoFilterBackend,)
    filter_class = filters.OrganizationFilter
    lookup_field = 'uuid'


class OrganizationUserViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                              mixins.DestroyModelMixin, mixins.ListModelMixin,
                              viewsets.GenericViewSet):
    queryset = models.OrganizationUser.objects.all()
    serializer_class = serializers.OrganizationUserSerializer
    permission_classes = (IsAuthenticated, permissions.OrganizationUserPermissions)
    filter_backends = (rf_filters.DjangoFilterBackend,)
    filter_class = filters.OrganizationUserFilter
    lookup_field = 'uuid'

    def get_queryset(self):
        queryset = super(OrganizationUserViewSet, self).get_queryset()

        if not self.request.user.is_staff:
            queryset = models.OrganizationUser.objects.filter(
                Q(user=self.request.user)
                |
                Q(organization__customer__roles__permission_group__user=self.request.user,
                  organization__customer__roles__role_type=CustomerRole.OWNER)
            )

        return queryset

    @detail_route(methods=['post'])
    def approve(self, request, uuid=None):
        instance = self.get_object()

        if instance.can_be_managed_by(request.user):
            instance.is_approved = True
            instance.save()
            return Response({'detail': "User request for joining the organization has been successfully approved"},
                            status=status.HTTP_200_OK)

        return Response({'detail': "User do no have permission to approve requests for joining the organization"},
                        status=status.HTTP_403_FORBIDDEN)

    @detail_route(methods=['post'])
    def reject(self, request, uuid=None):
        organization_user = self.get_object()

        if organization_user.can_be_managed_by(request.user):
            organization_user.is_approved = False
            organization_user.save()
            return Response({'detail': "User has been successfully rejected from the organization"},
                            status=status.HTTP_200_OK)

        return Response({'detail': "User do not have permission to reject from the organization"},
                        status=status.HTTP_403_FORBIDDEN)
