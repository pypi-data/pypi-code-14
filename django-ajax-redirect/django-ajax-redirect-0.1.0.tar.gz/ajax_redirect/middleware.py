from django.http import HttpResponseRedirect


class AjaxRedirectMiddleware(object):
    """
    Middleware for AJAX redirects in Django.

    Note: If installed, it will act on every AJAX requests.
    """

    def process_response(self, request, response):
        if request.is_ajax():
            if type(response) == HttpResponseRedirect:
                response.status_code = 278
        return response
