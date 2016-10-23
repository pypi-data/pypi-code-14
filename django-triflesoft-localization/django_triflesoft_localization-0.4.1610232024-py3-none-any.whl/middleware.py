from django.conf import settings
from django.utils import translation
from django.utils.cache import patch_vary_headers


PARAMETER_NAME = 'language_code'
COOKIE_NAME = 'language_code'


class LocalizationMiddleware(object):
    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request):
        from localization.models import Language

        if PARAMETER_NAME in request.GET:
            language_code = request.GET[PARAMETER_NAME]
        elif COOKIE_NAME in request.COOKIES:
            language_code = request.COOKIES[COOKIE_NAME]
        else:
            language_code = settings.LANGUAGE_CODE

        try:
            language = Language.objects.get(code__iexact=language_code)

            translation.activate(language.code)

            request.LANGUAGE_CODE = language.code
            request.LANGUAGE_ID = language.id
        except Language.DoesNotExist:
            pass

        response = self._get_response(request)

        if hasattr(response, 'set_cookie'):
            response.set_cookie(COOKIE_NAME, language_code, max_age=31536000)
            patch_vary_headers(response, ('Accept-Language',))

            if not 'Content-Language' in response:
                response['Content-Language'] = language_code

        return response
