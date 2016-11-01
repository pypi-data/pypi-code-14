# coding: utf-8

"""
    Example of a « chat application » by using `tornado_websocket.WebSocket` to handle communications,
    and Django's TemplateView for rendering.
"""

from django.views.generic import TemplateView

from tornado_websockets.websocket import WebSocket

tws = WebSocket('/my_chat')


class MyChat(TemplateView):
    """
        Proof of concept about a really simple web chat using websockets and supporting messages history
    """

    template_name = 'testapp/index.html'
    messages = []

    def __init__(self, **kwargs):
        super(MyChat, self).__init__(**kwargs)

        # Otherwise, 'self' parameter for method decorated by @ws_chat.on will not be defined
        tws.context = self

    @tws.on
    def connection(self, socket, data):
        # Send an history of the chat
        [socket.emit('new_message', __) for __ in self.messages]
        tws.emit('new_connection', '%s just joined the webchat.' % data.get('username', '<Anonymous>'))

    @tws.on
    def message(self, socket, data):
        message = {
            'username': data.get('username', '<Anonymous>'),
            'message': data.get('message', 'Empty message')
        }

        tws.emit('new_message', message)
        self.messages.append(message)

    @tws.on
    def clear_history(self, socket, data):
        """
            Called when a client wants to clear messages history.
            Used only for client-side JavaScript unit tests
        """

        self.messages = []
