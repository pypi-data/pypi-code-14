from __future__ import unicode_literals

from rest_framework.permissions import BasePermission, SAFE_METHODS


class OrganizationUserPermissions(BasePermission):
    """
    Allows full access to admin users and organization customer owners.
    User can remove his organization user only when it is not approved.
    """

    def has_permission(self, request, view):
        user = request.user
        if not user.is_staff and request.method == 'DELETE':
            organization_user = view.get_object()
            if not organization_user.is_approved:
                return True

            return organization_user.can_be_managed_by(user)

        return True
