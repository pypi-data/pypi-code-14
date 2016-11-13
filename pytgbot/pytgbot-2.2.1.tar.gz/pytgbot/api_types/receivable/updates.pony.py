from . import updates
from pony import orm as orm
db = orm.Database()


class Update(updates.Update, db.Entity):
    """
    This object represents an incoming update. Only one of the optional parameters can be present in any given update.

    https://core.telegram.org/bots/api#update
    """
    update_id = orm.Required(int)
    message = orm.Optional("Message")
    edited_message = orm.Optional("Message")
    inline_query = orm.Optional("InlineQuery")
    chosen_inline_result = orm.Optional("ChosenInlineResult")
    callback_query = orm.Optional("CallbackQuery")
# end class Update


class Message(updates.Message, db.Entity):
    """
    This object represents a message.

    https://core.telegram.org/bots/api#message
    """
    message_id = orm.Required(int)
    date = orm.Required(int)
    type = orm.Required("Chat")


    def __init__(self, message_id, date, chat, from_peer=None, forward_from=None, forward_from_chat=None, forward_date=None, reply_to_message=None, edit_date=None, text=None, entities=None, audio=None, document=None, photo=None, sticker=None, video=None, voice=None, caption=None, contact=None, location=None, venue=None, new_chat_member=None, left_chat_member=None, new_chat_title=None, new_chat_photo=None, delete_chat_photo=None, group_chat_created=None, supergroup_chat_created=None, channel_chat_created=None, migrate_to_chat_id=None, migrate_from_chat_id=None, pinned_message=None):
        """
        This object represents a message.

        https://core.telegram.org/bots/api#message


        Parameters:

        :param message_id: Unique message identifier
        :type  message_id: int

        :param date: Date the message was sent in Unix time
        :type  date: int

        :param chat: Conversation the message belongs to
        :type  chat: pytgbot.api_types.receivable.peer.Chat


        Optional keyword parameters:

        :keyword from_peer: Optional. Sender, can be empty for messages sent to channels
        :type    from_peer: pytgbot.api_types.receivable.peer.User

        :keyword forward_from: Optional. For forwarded messages, sender of the original message
        :type    forward_from: pytgbot.api_types.receivable.peer.User

        :keyword forward_from_chat: Optional. For messages forwarded from a channel, information about the original channel
        :type    forward_from_chat: pytgbot.api_types.receivable.peer.Chat

        :keyword forward_date: Optional. For forwarded messages, date the original message was sent in Unix time
        :type    forward_date: int

        :keyword reply_to_message: Optional. For replies, the original message. Note that the Message object in this field will not contain further reply_to_message fields even if it itself is a reply.
        :type    reply_to_message: Message

        :keyword edit_date: Optional. Date the message was last edited in Unix time
        :type    edit_date: int

        :keyword text: Optional. For text messages, the actual UTF-8 text of the message, 0-4096 characters.
        :type    text: str

        :keyword entities: Optional. For text messages, special entities like usernames, URLs, bot commands, etc. that appear in the text
        :type    entities: list of pytgbot.api_types.receivable.media.MessageEntity

        :keyword audio: Optional. Message is an audio file, information about the file
        :type    audio: pytgbot.api_types.receivable.media.Audio

        :keyword document: Optional. Message is a general file, information about the file
        :type    document: pytgbot.api_types.receivable.media.Document

        :keyword photo: Optional. Message is a photo, available sizes of the photo
        :type    photo: list of pytgbot.api_types.receivable.media.PhotoSize

        :keyword sticker: Optional. Message is a sticker, information about the sticker
        :type    sticker: pytgbot.api_types.receivable.media.Sticker

        :keyword video: Optional. Message is a video, information about the video
        :type    video: pytgbot.api_types.receivable.media.Video

        :keyword voice: Optional. Message is a voice message, information about the file
        :type    voice: pytgbot.api_types.receivable.media.Voice

        :keyword caption: Optional. Caption for the document, photo or video, 0-200 characters
        :type    caption: str

        :keyword contact: Optional. Message is a shared contact, information about the contact
        :type    contact: pytgbot.api_types.receivable.media.Contact

        :keyword location: Optional. Message is a shared location, information about the location
        :type    location: pytgbot.api_types.receivable.media.Location

        :keyword venue: Optional. Message is a venue, information about the venue
        :type    venue: pytgbot.api_types.receivable.media.Venue

        :keyword new_chat_member: Optional. A new member was added to the group, information about them (this member may be the bot itself)
        :type    new_chat_member: pytgbot.api_types.receivable.peer.User

        :keyword left_chat_member: Optional. A member was removed from the group, information about them (this member may be the bot itself)
        :type    left_chat_member: pytgbot.api_types.receivable.peer.User

        :keyword new_chat_title: Optional. A chat title was changed to this value
        :type    new_chat_title: str

        :keyword new_chat_photo: Optional. A chat photo was change to this value
        :type    new_chat_photo: list of pytgbot.api_types.receivable.media.PhotoSize

        :keyword delete_chat_photo: Optional. Service message: the chat photo was deleted
        :type    delete_chat_photo: bool

        :keyword group_chat_created: Optional. Service message: the group has been created
        :type    group_chat_created: bool

        :keyword supergroup_chat_created: Optional. Service message: the supergroup has been created. This field can‘t be received in a message coming through updates, because bot can’t be a member of a supergroup when it is created. It can only be found in reply_to_message if someone replies to a very first message in a directly created supergroup.
        :type    supergroup_chat_created: bool

        :keyword channel_chat_created: Optional. Service message: the channel has been created. This field can‘t be received in a message coming through updates, because bot can’t be a member of a channel when it is created. It can only be found in reply_to_message if someone replies to a very first message in a channel.
        :type    channel_chat_created: bool

        :keyword migrate_to_chat_id: Optional. The group has been migrated to a supergroup with the specified identifier. This number may be greater than 32 bits and some programming languages may have difficulty/silent defects in interpreting it. But it smaller than 52 bits, so a signed 64 bit integer or double-precision float type are safe for storing this identifier.
        :type    migrate_to_chat_id: int

        :keyword migrate_from_chat_id: Optional. The supergroup has been migrated from a group with the specified identifier. This number may be greater than 32 bits and some programming languages may have difficulty/silent defects in interpreting it. But it smaller than 52 bits, so a signed 64 bit integer or double-precision float type are safe for storing this identifier.
        :type    migrate_from_chat_id: int

        :keyword pinned_message: Optional. Specified message was pinned. Note that the Message object in this field will not contain further reply_to_message fields even if it is itself a reply.
        :type    pinned_message: Message
        """
        super(Message, self).__init__()