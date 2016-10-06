from messenger_sdk.templates import QuickReply


class BaseSampleTemplateResponse:
    @staticmethod
    def get_quick_reply(title, payload):
        quick_reply = QuickReply(title=title, payload=payload)

        return quick_reply

    @staticmethod
    def get_sender_action_template(sender_action='typing_on'):
        template = {
            'recipient': {
                'id': 358
            },
            'sender_action': sender_action
        }

        return template
