# -*- coding: utf-8 -*-
from django.utils.translation import ugettext as _
from re import escape

"""
# Routing Policy Explained

## Source

djmessenger/utils/default_routing_policy.py

## How routing in DJM works

1. DJM receives a payload from Facebook which contains possibly multiple
   `receiving.Messaging` object. Each `Messaging` object, we determine its
   `ReceivingType`:

   ```
   SIMPLE_TEXT
   QUICK_REPLY
   IMAGE
   AUDIO
   VIDEO
   FILE
   LOCATION
   STICKER
   POSTBACK
   AUTHENTICATION
   ACCOUNT_LINKING
   DELIVERED
   READ
   ECHO
   ```

2. In the policy, routers contains multiple router, each router defines which
   `ReceivingType` it handles.

   > Please note that 1 `ReceivingType` only has 1 router, if you defined multiple
     item for the same `ReceivingType`, only the first one will take effect

3. Each `ReceivingType` defines the Handlers (`djmessenger.handling` module) that
   should handle this `ReceivingType`.

   > You can provide args for the handler class's constructor as keyword
     arguments

4. For each Handler, you define multiple Senders (`djmessenger.sending` module)
   that will take care of sending something back to the user

   > You can provide args for the sender class's constructor as keyword
     arguments

   > The senders will be invoked iff the handler passes and was handled, if the
     `Messaging` does not meet Handler's handling prerequisite, it hence won't
     be handled and won't be sent to senders

   > You probably want to send back i18n'ed strings, so mark your sender text
     _()

       ```
       from django.utils.translation import ugettext as _
       ```

   > Be sure to use `re.escape` if your regex string contains chars that need to
     be escaped

## Example Explained

Here is a snippet in DJM's default routing policy

    ```
    {
        "type": "SIMPLE_TEXT",
        "handlers": [
            {
                "name": "djmessenger.handling.SimpleTextBaseHandler",
                "args": {
                    "regex": ""
                },
                "senders": [
                    {
                        "name": "djmessenger.sending.SimpleMessageSender",
                        "args": {
                            "text": _(
                                "Thanks for your message, we will get back to you soon")
                        }
                    }
                ]
            },
            {
                "name": "djmessenger.handling.SimpleTextBaseHandler",
                "args": {
                    "regex": "^你好$"
                },
                "senders": [
                    {
                        "name": "djmessenger.sending.SimpleMessageSender",
                        "args": {
                            "text": "您也好"
                        }
                    }
                ]
            }
        ]
    },
    ```

You can vision it very easily that:

1. A `Messaging` object that was determined as `SIMPLE_TEXT` type will be sent
   to `djmessenger.handling.SimpleTextBaseHandler` with different regex
2. The first `SimpleTextBaseHandler` has no regex arg, so it will just pass and
   the `SimpleMessageSender` simply sends back the `text`
3. The second `SimpleTextBaseHandler` has regex defined, so if the user sends
   the bot a `SIMPLE_TEXT` that matches this regex, this handler will handle it
   and then sender will be invoked

## Builtin Handlers

See Handlers for more details

"""
DJM_DEFAULT_ROUTING_POLICY = \
    {
        "routers": [
            {
                "type": "DEFAULT",
                "handlers": [
                    {
                        "name": "djmessenger.handling.SaveMessagingHandler",
                        "args": {},
                        "senders": []
                    },
                    {
                        "name": "djmessenger.handling.UserProfileHandler",
                        "args": {},
                        "senders": []
                    }
                ]
            },
            {
                "type": "STICKER",
                "handlers": [
                    {
                        "name": "djmessenger.handling.ThumbUpHandler",
                        "args": {},
                        "senders": [
                            {
                                "name": "djmessenger.sending.SimpleMessageSender",
                                "args": {
                                    "text": _("Thank you for your thumb!!!")
                                }
                            },
                            {
                                "name": "djmessenger.sending.MultimediaSender",
                                "args": {
                                    "sending_type": "image",
                                    "url": "https://dl.dropboxusercontent.com/u/717667/icons/betatesting.png"
                                }
                            }
                        ]
                    }
                ]
            },
            {
                "type": "SIMPLE_TEXT",
                "handlers": [
                    {
                        "name": "djmessenger.handling.SimpleTextBaseHandler",
                        "args": {
                            "regex": "^你好$"
                        },
                        "senders": [
                            {
                                "name": "djmessenger.sending.SimpleMessageSender",
                                "args": {
                                    "text": "您也好"
                                }
                            }
                        ]
                    },
                    {
                        "name": "djmessenger.handling.SimpleTextBaseHandler",
                        "args": {
                            "regex": "^hi$"
                        },
                        "senders": [
                            {
                                "name": "djmessenger.sending.SimpleMessageSender",
                                "args": {
                                    "text": _(
                                        "Thanks for your message, we will get back to you soon")
                                }
                            }
                        ]
                    }
                ]
            },
            {
                "type": "LOCATION",
                "handlers": [
                    {
                        "name": "djmessenger.handling.LocationHandler",
                        "args": {},
                        "senders": []
                    }
                ]
            }
        ]
    }
