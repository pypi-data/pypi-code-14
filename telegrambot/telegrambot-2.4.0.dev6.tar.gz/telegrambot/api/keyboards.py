""" Copyright 2015 Will Boyce """
from __future__ import print_function, unicode_literals

from telegrambot.api.base import APIObject
from telegrambot.api.message import Message
from telegrambot.api.user import User


class ReplyKeyboardMarkup(APIObject):
    """
        This object represents a custom keyboard with reply options.

        keyboard	        Array of Array of String	Array of button rows, each represented by an Array of Strings
        resize_keyboard	    Boolean	                    (Optional) Requests clients to resize the keyboard vertically
                                                        for optimal fit (e.g., make the keyboard smaller if there are
                                                        just two rows of buttons). Defaults to false, in which case the
                                                        custom keyboard is always of the same height as the app's
                                                        standard keyboard.
        one_time_keyboard	Boolean	                    (Optional) Requests clients to hide the keyboard as soon as it's
                                                        been used. Defaults to false.
        selective	        Boolean	                    (Optional) Use this parameter if you want to show the keyboard
                                                        to specific users only. Targets:
                                                            1) users that are @mentioned in the text of the
                                                                Message object;
                                                            2) if the bot's message is a reply (has reply_to_message_id)
                                                                then sender of the original message.
    """
    _api_attrs = (
        ('keyboard', [[str]], TypeError),
        ('resize_keyboard', bool, False),
        ('one_time_keyboard', bool, False),
        ('selective', bool, False),
    )


class ReplyKeyboardHide(APIObject):
    """
        Upon receiving a message with this object, Telegram clients will hide the current custom keyboard and display
        the default letter-keyboard. By default, custom keyboards are displayed until a new keyboard is sent by a bot.
        An exception is made for one-time keyboards that are hidden immediately after the user presses a button.

        hide_keyboard	True	    Requests clients to hide the custom keyboard
        selective	    Boolean	    (Optional) Use this parameter if you want to hide keyboard for specific users only.
                                    Targets:
                                        1) users that are @mentioned in the text of the Message object;
                                        2) if the bot's message is a reply (has reply_to_message_id),
                                            sender of the original message.
    """
    _api_attrs = (
        ('hide_keyboard', bool, True),
        ('selective', bool, False),
    )


class CallbackQuery(APIObject):
    """
        This object represents an incoming callback query from a callback button in an inline keyboard. If the button
        that originated the query was attached to a message sent by the bot, the field message will be presented.
        If the button was attached to a message sent via the bot (in inline mode), the field inline_message_id
        will be presented.

        id	String	Unique identifier for this query
        from	            User	Sender
        message	            Message	(Optional) Message with the callback button that originated the query.
                                    Note that message content and message date will not be available if the
                                    message is too old
        inline_message_id	String	(Optional) Identifier of the message sent via the bot in inline mode,
                                    that originated the query
        data	            String	Data associated with the callback button. Be aware that a bad client
                                    can send arbitrary data in this field
    """
    _api_attrs = (
        ('from', User, True),
        ('message', Message, False),
        ('inline_message_id', str, False),
        ('data', str, False)
    )


class InlineKeyboardButton(APIObject):
    """
        This object represents one button of an inline keyboard. You *must* use exactly one of the optional fields.

        text	            String	Label text on the button
        url	                String	(Optional) HTTP url to be opened when button is pressed
        callback_data	    String	(Optional) Data to be sent in a callback query to the bot when button is pressed
        switch_inline_query	String	(Optional) If set, pressing the button will prompt the user to select one of their
                                    chats, open that chat and insert the bot's username and the specified inline query
                                    in the input field.
                                    Can be empty, in which case just the bot's username will be inserted.
    """
    _api_attrs = (
        ('text', str, True),
        ('url', str, False),
        ('callback_data', str, False),
        ('switch_inline_query', str, False)
    )


class InlineKeyboardMarkup(APIObject):
    """
        This object represents an inline keyboard that appears right next to the message it belongs to.
    """
    _api_attrs = (
        ('inline_keyboard', [[InlineKeyboardButton]], True)
    )


class ForceReply(APIObject):
    """
        Upon receiving a message with this object, Telegram clients will display a reply interface to the user
        (act as if the user has selected the bot's message and tapped 'Reply').

        force_reply	    True	    Shows reply interface to the user, as if they manually selected the bot's message
                                    and tapped 'Reply'
        selective	    Boolean	    (Optional) Use this parameter if you want to force reply from specific users only.
                                    Targets:
                                        1) users that are @mentioned in the text of the Message object;
                                        2) if the bot's message is a reply (has reply_to_message_id),
                                            sender of the original message.
    """
    _api_attrs = (
        ('force_reply', bool, True),
        ('selective', bool, False),
    )