#!/usr/bin/env python3

       ##############
      # SKYCHAT API #
     # IN PYTHON  #
    ##############

import requests
import json
from socketIO_client import SocketIO, LoggingNamespace
from time import sleep


class SkyChatClient:
    """ Standard client for the SkyChat v2.0 """
    def __init__(self, pseudo=None, password=None, room=0):
        """ ...

        pseudo   -- account name
        password -- password (why do I even document that ?)
            | If pseudo & password are empty, you will login as a dirty Hamster
        room     -- Number of the room where you want yur bot to be
        """
        self.pseudo      = pseudo
        self.credentials = None
        self.room        = int(room)
        self.logged      = False
        self.on_creation()
        if password:
            self._get_login_token(pseudo, password)
        self._connect()

    def _get_login_token(self, pseudo, password):
        """ Sends login info to get the token... All the info are stored in
        self.credentials """
        self.credentials = json.loads(requests.post("http://redsky.fr/ajax/account/api2.php", {'pseudo' : pseudo, 'pass' : password}).text)

    def _connect(self):
        """ Creates the websocket, the message handler, and logs you in your
        room
        """
        self.ws = SocketIO('redsky.fr', 8056, LoggingNamespace)
        self.ws.on('message', self._message_handler)
        self.ws.on('connected_list', self.on_connected_list)
        self.ws.on('typing_list', self.on_typing_list)
        self.ws.on('pseudo_info', self._pseudo_info_handler)
        self.ws.on('room_update', self.on_room_update)
        self.ws.on('mouse_position', self.on_mouse_position)

        self.ws.emit('log', self.credentials)
        self.msgsend('/join %d' % (self.room))
        
        if not self.credentials:
            self.on_connect()

    def msgsend(self, msg):
        """ Sends a standard message in the current room

        msg -- text to send
        """
        self.ws.emit('message', {'message' : msg})

    def pmsend(self, target, msg):
        """ Sends a private message to a user

        target -- target user name (not case sensitive)
        msg    -- text to send
        """
        self.msgsend("/mp %s %s" % (target, msg))

    def set_typing(self, state):
        """ Indicates to the server that you started or stopped typing

        state -- boolean, indicates whether you start or stop
        """
        self.ws.emit('typing', {'currently_typing' : state})

    def _message_handler(self, msg):
        """ Pre-treats messages, before passing it to self.on_message 

        msg -- the received message, in form of a dict (if it is of another
               type, it will be refused
        """
        if type(msg) != dict:
            return
        if 'old' in msg:
            self.on_old_message(msg)
        elif msg['message_type'] == 'user_message':
            self.on_message(msg)
        elif msg['message_type'] == 'user_mp':
            self.on_private_message(msg)


    def _pseudo_info_handler(self, msg):
        if msg['logged'] and self.credentials and not self.logged:
            self.on_connect()
            self.logged = True
        self.on_pseudo_info(msg)

    def on_creation(self):
        """ Called when the client is created
        Useful to add elements to __init__
        Can be redefined """
        pass

    def on_connect(self):
        """ Called when the client connects
        Can be redefined """
        pass

    def on_message(self, msg):
        """ Called when a message is received
        Can be redefined """
        pass

    def on_private_message(self, msg):
        """ Called when a private message is received
        Can be redefined """
        pass

    def on_old_message(self, msg):
        """ Called when old messages are loaded, at the connection
        Can be redefined """
        pass

    def on_pseudo_info(self, msg):
        """ Called when the server gives new infos about the pseudo
        Can be redefined """
        pass

    def on_room_update(self, msg):
        """ Called when something changes in the room
        Can be redefined  """
        pass

    def on_connected_list(self, msg):
        """ Called when the connected list is update, when somebody joined or
        leaved
        Can be redefined """
        pass

    def on_typing_list(self, msg):
        """ Called when the typing list is updated
        Can be redefined """
        pass

    def on_mouse_position(self, msg):
        """ Called when someone's mouse curser moves
        Totally useless, I know...
        But quite cool right ?
        Can be redefined """
        pass


    def run(self, duration=600):
        while True:
            sleep(duration)
            self.msgsend("/join %d" % (self.room))

