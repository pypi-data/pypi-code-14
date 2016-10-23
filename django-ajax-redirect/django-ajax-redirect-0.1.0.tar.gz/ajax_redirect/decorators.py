from django.utils.decorators import decorator_from_middleware

from .middleware import AjaxRedirectMiddleware

# Decorator for AJAX redirects in Django.
# Note: Can be used in conjunction with Django `method_decorator` helper.
ajax_redirect = decorator_from_middleware(AjaxRedirectMiddleware)
