import logging
import json

from django.views import generic
from django.http.response import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from djmessenger.receiving import Callback
from djmessenger.handling import BaseHandler
from djmessenger.sending import CommonSender


logger = logging.getLogger(__name__)


class DJMBotView(generic.View):
    def get(self, request, *args, **kwargs):
        verify_token = self.request.GET.get('hub.verify_token', None)
        challenge = self.request.GET.get('hub.challenge', None)
        if verify_token and challenge:
            return HttpResponse(challenge)
        else:
            logger.error('Either verify_token [%s] or challenge [%s] not found '
                         'in url parameter' % (verify_token, challenge))
            return HttpResponse('Error, invalid token')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        body = self.request.body.decode('utf-8')
        incoming_message = json.loads(body)
        # logger.debug('DJM_HANDLERS: %s' % DJM_HANDLERS)
        try:
            callback = Callback.deserialize(incoming_message)
            assert isinstance(callback, Callback)
            # save user profile if settings to True
            for entry in callback.entry:
                for messaging in entry.messaging:
                    self._handle_messaging(messaging)
        except Exception as e:
            logging.exception('Got exception on post...')
            logger.error('Failed to handle the message because %s' % e)
        return HttpResponse()

    def _handle_messaging(self, messaging):
        from djmessenger.routing import policy

        logger.debug('*****************************************')
        logger.debug('*****    Start of a new message     *****')
        logger.debug('*****************************************')
        logger.debug(
            'Ready to process messaging of ReceivingType %s: %s' %
            (messaging.get_receiving_type(), messaging.serialize()))
        handlers = policy.get_handlers(messaging.get_receiving_type())
        logger.debug('Got applicable routing handler classes from policy: %s'
                     % handlers)
        # loop through corresponding handlers
        for handler in handlers:
            if not issubclass(handler.get_class(), BaseHandler):
                continue
            handler_instance = handler.get_class()(messaging,
                                                   **handler.get_args())
            handler_name = handler.get_class().__name__
            logger.debug('-->  Start of handling process to handler %s for '
                         'messaging %s <--'
                         % (handler_name, messaging.serialize()))
            if handler_instance.should_handle():
                handler_instance.handle()

                senders = policy.get_senders(messaging.get_receiving_type(),
                                             handler)
                logger.debug('Handler %s is done, ready to send using senders: '
                             '%s' % (handler_name, senders))
                for sender in senders:
                    if not issubclass(sender.get_class(), CommonSender):
                        continue
                    sender_name = sender.get_class().__name__
                    logger.debug(
                        '-->  Start of sending process to sender %s for '
                        'messaging %s <--'
                        % (sender_name, messaging.serialize()))
                    sender_instance = sender.get_class()(handler_instance,
                                                         **sender.get_args())
                    sender_instance.send()
                    logger.debug('-->  End of sending process to %s  <--'
                                 % sender_name)
            else:
                logger.debug('The messaging was not being handled by handler %s'
                             ', so no sending will be performed' %
                             handler_name)
            logger.debug('-->  End of handling process to %s  <--'
                         % handler_name)
        logger.debug('*****************************************')
        logger.debug('*****  End of a processing message  *****')
        logger.debug('*****************************************')
