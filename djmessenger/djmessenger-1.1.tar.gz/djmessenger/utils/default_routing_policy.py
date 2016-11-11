# -*- coding: utf-8 -*-
"""
This is a sample routing policy to demonstrate how to define a routing policy.

From the following sample, we can observe that

1. A policy has a rules and it contains a list of :class:`djmessenger.routing.Rule`
2. Each :class:`djmessenger.routing.Rule` defines

    2.1 type: :class:`djmessenger.receiving.ReceivingType` indicates what kinds
    of :class:`djmessenger.receiving.Messaging` this Rule should be applied upon

    2.2 name: Rule name

    2.3 filters: A list of subclass of :class:`djmessenger.filtering.BaseFilter`
    that will be applied to the message, if any of the filters fails, the whole
    Rule will be skipped

    2.4 handlers: A list of subclass of :class:`djmessenger.handling.BaseHandler`
    that will be applied to the message

    2.5 repliers: A list of subclass of :class:`djmessenger.replying.CommonReplier`
    that will take a message and reply something back

3. Filter, Handler and Repliers can take arguments, for example,

::

    class SimpleMessageReplier(CommonReplier):
        custom_obj_map = {
            "localized_string": (LocalizedString, object)
        }
        def __init__(self, localized_string):
            super().__init__()
            self.localized_string = localized_string

:class:`djmessenger.replying.SimplyMessageReplier` requires an instance
of :class:`djmessenger.utils.utils.LocalizedString` as argument. Therefore,
in the policy we can see

::

    {
        "name": "djmessenger.replying.SimpleMessageReplier",
        "args": {
            "localized_string": {
                "base_string": "Thank you for your thumb!!!",
                "translations": {
                    "zh_TW": "謝謝您的讚",
                }
            }
        }
    },

which indicates that the replier requires an argument and provide the data


"""
DJM_DEFAULT_ROUTING_POLICY = \
    {
        "rules": [
            {
                "type": "DEFAULT",
                "name": "default rule",
                "filters": [
                    {
                        "name": "djmessenger.filtering.TimeFilter",
                        "args": {
                            "start_time": "2016-1-1T00:00:00Z-0800",
                            "end_time": "2017-1-1T01:00:00Z-0800"
                        }
                    }
                ],
                "handlers": [
                    {
                        "name": "djmessenger.handling.UserProfileHandler",
                    },
                    {
                        "name": "djmessenger.handling.SaveMessagingHandler",
                    }
                ]
            },
            {
                "type": "STICKER",
                "name": "ThumbUp Rule",
                "filters": [
                    {
                        "name": "djmessenger.filtering.ThumbUpFilter"
                    }
                ],
                "handlers": [
                    {
                        "name": "djmessenger.handling.ThumbUpHandler",
                    }
                ],
                "repliers": [
                    {
                        "name": "djmessenger.replying.SimpleMessageReplier",
                        "args": {
                            "localized_string": {
                                "base_string": "Thank you for your thumb!!!",
                                "translations": {
                                    "zh_TW": "謝謝您的讚",
                                }
                            }
                        }
                    },
                    {
                        "name": "djmessenger.replying.ImageReplier",
                        "args": {
                            "url": "https://dl.dropboxusercontent.com/u/717667/icons/betatesting.png"
                        }
                    }
                ]
            },
            {
                "type": "SIMPLE_TEXT",
                "name": "Hello Chinese Rule",
                "filters": [
                    {
                        "name": "djmessenger.filtering.SimpleTextRegexFilter",
                        "args": {
                            "regex": "^你好$"
                        }
                    }
                ],
                "repliers": [
                    {
                        "name": "djmessenger.replying.SimpleMessageReplier",
                        "args": {
                            "localized_string": {
                                "base_string": "您也好",
                                "translations": {
                                    "en_US": "Hello to you, too!"
                                }
                            }
                        }
                    }
                ]
            },
            {
                "type": "SIMPLE_TEXT",
                "name": "Hi Rule",
                "filters": [
                    {
                        "name": "djmessenger.filtering.SimpleTextRegexFilter",
                        "args": {
                            "regex": "^hi$"
                        },
                    }
                ],
                "repliers": [
                    {
                        "name": "djmessenger.replying.SimpleMessageReplier",
                        "args": {
                            "localized_string": {
                                "base_string":
                                    "Hi you, too!",
                                "translations": {
                                    "zh_TW": "您也好"
                                }
                            }
                        }
                    }
                ]
            },
            {
                "type": "SIMPLE_TEXT",
                "name": "buttons Rule",
                "filters": [
                    {
                        "name": "djmessenger.filtering.SimpleTextRegexFilter",
                        "args": {
                            "regex": "^buttons$"
                        },
                    }
                ],
                "repliers": [
                    {
                        "name": "testapp.sending.MyButtonSender",
                        "args": {
                            "localized_string": {
                                "base_string": "Please choose a button",
                                "translations": {
                                    "zh_TW": "請選擇一個按鈕"
                                }
                            }
                        }
                    }
                ]
            },
            {
                "type": "LOCATION",
                "name": "Location Rule",
                "filters": [
                    {
                        "name": "djmessenger.filtering.LocationFilter"
                    }
                ],
                "handlers": [
                    {
                        "name": "djmessenger.handling.LocationHandler",
                    }
                ]
            },
            {
                "type": "PERSISTENT_MENU_ONE",
                "name": "PM1 Rule",
                "repliers": [
                    {
                        "name": "djmessenger.replying.SimpleMessageReplier",
                        "args": {
                            "localized_string": {
                                "base_string": "This is help info",
                                "translations": {
                                    "zh_TW": "這是幫助訊息"
                                }
                            }
                        }
                    },
                    {
                        "name": "testapp.sending.MyQuickReplySender",
                        "args": {
                            "localized_string": {
                                "base_string": "Please choose a QR",
                                "translations": {
                                    "zh_TW": "請選擇快速回覆"
                                }
                            }
                        }
                    }
                ]
            },
            {
                "type": "QUICK_REPLY",
                "name": "QR1 Rule",
                "handlers": [
                    {
                        "name": "testapp.handling.MyQuickReplyHandler",
                    }
                ],
                "repliers": [
                    {
                        "name": "djmessenger.replying.SimpleMessageReplier",
                        "args": {
                            "localized_string": {
                                "base_string": "Thanks for the quick reply",
                                "translations": {
                                    "zh_TW": "謝謝您的快速回覆"
                                }
                            }
                        }
                    }
                ]
            }
        ]
    }
