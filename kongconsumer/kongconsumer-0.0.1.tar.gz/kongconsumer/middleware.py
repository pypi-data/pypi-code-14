from django.contrib.auth.middleware import RemoteUserMiddleware


class KongConsumerMiddleware(RemoteUserMiddleware):
    """
    Middleware to login a user based on the upstream X-Consumer-Username header
    used by Kong.
    """
    header = 'HTTP_X_CONSUMER_USERNAME'

    def process_request(self, request):
        super().process_request(request)

        if self.header in request.META and request.user.is_authenticated():
            request._dont_enforce_csrf_checks = True
