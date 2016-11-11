import logging
import json

from django.views import generic
from django.http.response import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from djmessenger.receiving import Callback
from djmessenger import settings


logger = logging.getLogger(__name__)


class DJMBotView(generic.View):
    def get(self, request, *args, **kwargs):
        """
        This will be called when Facebook verifies the endpoint
        """
        verify_token = self.request.GET.get('hub.verify_token', None)
        challenge = self.request.GET.get('hub.challenge', None)
        logger.debug('Got FB verification request with verify token %s '
                     'and challenge %s' % (verify_token, challenge))
        if verify_token and challenge and verify_token == settings.DJM_ENDPOINT_VERIFY_TOKEN:
            return HttpResponse(challenge)
        else:
            logger.error('Either verify_token [%s] or challenge [%s] not found '
                         'in url parameter' % (verify_token, challenge))
            return HttpResponse('Error, invalid token')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        All Facebook callback will reach here
        """
        logger.debug('*****************************************')
        logger.debug('*****    Start of a new callback    *****')
        logger.debug('*****************************************')
        try:
            callback = Callback.get_instance(request)
            assert isinstance(callback, Callback)
            # save user profile if settings to True
            for entry in callback.entry:
                for messaging in entry.messaging:
                    self._handle_messaging(messaging)
        except Exception as e:
            logging.exception('Got exception on post...')
            logger.error('Failed to handle the message because %s' % e)
        logger.debug('*****************************************')
        logger.debug('*****     End of the callback       *****')
        logger.debug('*****************************************')
        return HttpResponse()

    def _handle_messaging(self, messaging):
        from djmessenger.routing import Policy

        policy = Policy.get_instance(settings.DJM_ROUTING_POLICY)
        policy.apply(messaging)
