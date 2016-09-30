from .settings import api_settings


class BasePermission(object):

    def has_permission(self, message):
        return True

    def has_object_permission(self, message, obj):
        return True

    def has_permission(self, action, pk, data):
        return True

class AllowAny(BasePermission):

    def has_permission(self, message):
        return True

class IsAuthenticated(BasePermission):

    def has_permission(self, message):
        return message.user and message.user.is_authenticated

class PermissionsError(Exception):

    @property
    def detail(self):
        return str(self)

class PermissionConsumerMixin:

    permission_classes = api_settings.DEFAULT_PERMISSION_CLASSES

    def get_permissions(self):
        return [ permission() for permission in self.permission_classes ]

    def check_permissions(self, message):
        for permission in self.get_permissions():
            if not permission.has_permission(message):
                self.permission_denied(message)


    def check_object_permissions(self, message, obj):
        for permission in self.get_permissions():
            if not permission.has_object_permission(message, obj):
                self.permission_denied(message)

    def permission_denied(self, message):
        raise PermissionsError("Permission Denied")
