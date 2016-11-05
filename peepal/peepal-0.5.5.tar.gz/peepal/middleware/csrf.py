import hmac

from ..web import HttpError


class AntiCsrf:
    def __init__(self, check_origin=False, csrf_cookie_name='csrftoken', csrf_header_name='HTTP_X_CSRFTOKEN'):
        self.check_origin = check_origin
        self.csrf_cookie_name = csrf_cookie_name
        self.csrf_header_name = csrf_header_name

    def __call__(self, controller, next):
        request = controller.request

        # Assume that anything not defined as 'safe' by RC2616 needs protection.
        if request.method not in ('GET', 'HEAD', 'OPTIONS', 'TRACE'):
            csrf_cookie = request.get_cookie(self.csrf_cookie_name)
            if csrf_cookie is None or len(csrf_cookie) < 16:
                self._reject(request, reason="CSRF cookie not set or too short.")

            csrf_token = request.form_data.get(self.csrf_cookie_name) or request.environ.get(self.csrf_header_name)
            if csrf_token != csrf_cookie:
                self._reject(request, reason="CSRF token missing or incorrect.")

            if self.check_origin:
                origin = request.environ.get('HTTP_ORIGIN')
                if origin is not None and not hmac.compare_digest(origin.lower(), request.scheme + '://' + request.host.lower()):
                    # If the Origin header is present, the server must reject any requests
                    # whose Origin header contains an undesired value (including null).
                    self._reject(request, reason="Origin checking failed")

        next()

    def _reject(self, request, reason):
        raise HttpError(403, reason)
