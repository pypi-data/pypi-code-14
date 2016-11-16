# -*- coding:utf-8 -*-
class BasePermission(object):
    """
    Taken from django-rest-framework
    A base class from which all permission classes should inherit.
    """

    def has_permission(self, view):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        return True


class AllowAny(BasePermission):
    """
    Allow any access.
    This isn't strictly required, since you could use an empty
    permission_classes list, but it's useful because it makes the intention
    more explicit.
    """

    def has_permission(self, view):
        return True
