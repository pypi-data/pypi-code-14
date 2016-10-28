from django.http.response import HttpResponseRedirect
from django.conf import settings

from tradenity.sdk import Tradenity
from tradenity.sdk.exceptions import SessionExpiredException


def reset_session():
    Tradenity.reset_current_session()
    return HttpResponseRedirect("/")


class SessionExpiryHandlerMiddleware(object):

    def process_exception(self, request, exception):
        if isinstance(exception, SessionExpiredException):
            if hasattr(settings, 'on_session_expiry') and callable(settings.on_session_expiry):
                return settings.on_session_expiry()
            else:
                return reset_session()
