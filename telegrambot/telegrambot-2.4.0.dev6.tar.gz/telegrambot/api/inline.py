""" Copyright 2015 Will Boyce """
from __future__ import print_function, unicode_literals

from telegrambot.api.base import APIObject
from telegrambot.api.keyboards import InlineKeyboardMarkup
from telegrambot.api.media import Location
from telegrambot.api.user import User


class InlineQuery(APIObject):
    """
        This object represents an incoming inline query. When the user sends an empty query,
        your bot could return some default or trending results.

        id	        String	    Unique identifier for this query
        from	    User	    Sender
        location	Location	(Optional) Sender location, only for bots that request user location
        query	    String	    Text of the query
        offset	    String	    Offset of the results to be returned, can be controlled by the bot
    """
    _api_attrs = (
        ('id', str, TypeError),
        ('from', User, TypeError),
        ('location', Location, None),
        ('query', str, TypeError),
        ('offset', str, TypeError)
    )


class ChosenInlineResult(APIObject):
    """
        Represents a result of an inline query that was chosen by the user and sent to their chat partner.

        result_id	        String	    The unique identifier for the result that was chosen
        from	            User	    The user that chose the result
        location	        Location	(Optional) Sender location, only for bots that require user location
        inline_message_id	String	    (Optional) Identifier of the sent inline message.
                                        Available only if there is an inline keyboard attached to the message.
                                        Will be also received in callback queries and can be used to edit the message.
        query	            String	    The query that was used to obtain the result
    """
    _api_attrs = (
        ('result_id', str, TypeError),
        ('from', User, TypeError),
        ('location', Location, None),
        ('inline_message_id', str, None),
        ('query', str, TypeError),
    )


class InputMessageContent(APIObject):
    """
        This object represents the content of a message to be sent as a result of an inline query.
    """
    pass


class InputTextMessageContent(InputMessageContent):
    """
        Represents the content of a text message to be sent as the result of an inline query.

        message_text	            String	Text of the message to be sent, 1-4096 characters
        parse_mode	                String	(Optional) Send Markdown or HTML, if you want Telegram apps to show bold,
                                            italic, fixed-width text or inline URLs in your bot's message.
        disable_web_page_preview	Boolean	(Optional) Disables link previews for links in the sent message
    """
    _api_attrs = (
        ('message_text', str, TypeError),
        ('parse_mode', str, None),
        ('disable_web_page_preview', bool, None)
    )


class InputLocationMessageContent(InputMessageContent):
    """
        Represents the content of a location message to be sent as the result of an inline query.

        latitude	Float	Latitude of the location in degrees
        longitude	Float	Longitude of the location in degrees
    """
    _api_attrs = (
        ('latitude', float, TypeError),
        ('longitude', float, TypeError)
    )


class InputVenueMessageContent(InputMessageContent):
    """
        Represents the content of a venue message to be sent as the result of an inline query.

        latitude	    Float	Latitude of the venue in degrees
        longitude	    Float	Longitude of the venue in degrees
        title	        String	Name of the venue
        address	        String	Address of the venue
        foursquare_id	String	(Optional) Foursquare identifier of the venue, if known
    """
    _api_attrs = (
        ('latitude', float, TypeError),
        ('longitude', float, TypeError),
        ('title', str, TypeError),
        ('address', str, TypeError),
        ('foursquare_id', str, None)
    )


class InputContactMessageContent(InputMessageContent):
    """
        Represents the content of a contact message to be sent as the result of an inline query.

        phone_number	String	Contact's phone number
        first_name	    String	Contact's first name
        last_name	    String	(Optional) Contact's last name
    """
    _api_attrs = (
        ('phone_number', str, TypeError),
        ('first_name', str, TypeError),
        ('last_name', str, None)
    )


class InlineQueryResult(APIObject):
    """
        This object represents one result of an inline query.
    """
    pass


class InlineQueryResultArticle(InlineQueryResult):
    """
        Represents a link to an article or web page.

        type	                String	                Type of the result, must be article
        id	                    String	                Unique identifier for this result, 1-64 Bytes
        title	                String	                Title of the result
        input_message_content	InputMessageContent	    Content of the message to be sent
        reply_markup	        InlineKeyboardMarkup	(Optional) Inline keyboard attached to the message
        url	                    String	                (Optional) URL of the result
        hide_url	            Boolean	                (Optional) Pass True, if you don't want the URL to be shown in the message
        description	            String	                (Optional) Short description of the result
        thumb_url	            String	                (Optional) Url of the thumbnail for the result
        thumb_width	            Integer	                (Optional) Thumbnail width
        thumb_height	        Integer	                (Optional) Thumbnail height
    """
    _api_attrs = (
        ('type', str, TypeError),
        ('id', str, TypeError),
        ('title', str, TypeError),
        ('input_message_content', InputMessageContent, TypeError),
        ('reply_markup', InlineKeyboardMarkup, None),
        ('url', str, None),
        ('hide_url', bool, False),
        ('description', str, None),
        ('thumb_url', str, None),
        ('thumb_width', int, None),
        ('thumb_height', int, None),
    )


class InlineQueryResultPhoto(InlineQueryResult):
    pass


class InlineQueryResultGif(InlineQueryResult):
    pass


class InlineQueryResultMpeg4Gif(InlineQueryResult):
    pass


class InlineQueryResultVideo(InlineQueryResult):
    pass


class InlineQueryResultAudio(InlineQueryResult):
    pass


class InlineQueryResultVoice(InlineQueryResult):
    pass


class InlineQueryResultDocument(InlineQueryResult):
    pass


class InlineQueryResultLocation(InlineQueryResult):
    pass


class InlineQueryResultVenue(InlineQueryResult):
    pass


class InlineQueryResultContact(InlineQueryResult):
    pass