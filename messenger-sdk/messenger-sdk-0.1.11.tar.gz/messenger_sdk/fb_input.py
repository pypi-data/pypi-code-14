class FbInput:
    @staticmethod
    def create_text_message(text, quick_reply_payload=None):
        sender_id = 358
        recipient_id = 588667681307355
        message = {
            'seq': 53,
            'mid': 'mid.1466750926480:b2598e311e5ad42d71',
            'text': text
        }
        if quick_reply_payload:
            message.update({
                'quick_reply': {
                    'payload': quick_reply_payload
                }
            })
        template = {
            'sender': {
                'id': sender_id
            },
            'message': message,
            'recipient': {
                'id': recipient_id
            },
            'timestamp': 1466750926487
        }

        return template

    @staticmethod
    def create_attachment_message():
        sender_id = 358
        recipient_id = 588667681307355
        template = {
            'sender': {
                'id': sender_id
            },
            'recipient': {
                'id': recipient_id
            },
            'message': {
                'mid': 'mid.1466751206432:f290a56f73f8b02b63',
                'seq': 55,
                'sticker_id': 369239263222822,
                'attachments': [{
                    'type': 'image',
                    'payload': {
                        'url': 'https://example.com/image.png'
                    }
                }]
            },
            'timestamp': 1466750926487}

        return template

    @staticmethod
    def create_delivery():
        sender_id = 358
        recipient_id = 588667681307355
        template = {
            'sender': {
                'id': sender_id
            },
            'recipient': {
                'id': recipient_id
            },
            'delivery': {
                'seq': 12,
                'mids': ['mid.1466675298251:7204294a89a4aae828'],
                'watermark': 1466675298280
            },
            'timestamp': 0}

        return template

    @staticmethod
    def create_attachment_message_with_coordinates():
        template = {
            'timestamp': 1472722892136,
            'message': {
                'attachments': [{
                    'payload': {
                        'coordinates': {
                            'lat': 52.440433969359,
                            'long': 16.912738256133
                        }
                    },
                    'url': 'https://www.facebook.com/l.php?u=https%3A%2F%2Fwww.bing.com%2Fmaps%2Fdefault.aspx%3Fv%3D2%26pc%3DFACEBK%26mid%3D8100%26where1%3DPi%25C4%2585tkowska%2B200%252C%2B61-691%2BPoznan%252C%2BPoland%26FORM%3DFBKPL1%26mkt%3Den-US&h=gAQExQLq5&s=1&enc=AZMaa60a3PRmvr7cCq_NxbB0_9bDCkvMtjEyVPUXdI8k_Fn_Dc3azA1N38Rf1gALRVZb8Z63q1iL3iKUXyp3h7attTPdIn1eM3Vsg6zjrFutHw',
                    'title': 'Foo location',
                    'type': 'location'
                }],
                'mid': 'mid.1472722891670:f5daf1db754cb91616',
                'seq': 18
            },
            'sender': {
                'id': '1072879492798443'
            },
            'recipient': {
                'id': '319022018450028'
            }
        }

        return template

    @staticmethod
    def create_postback(payload):
        sender_id = 358
        recipient_id = 588667681307355
        template = {
            'sender': {
                'id': sender_id
            },
            'recipient': {
                'id': recipient_id
            },
            'postback': {
                'payload': payload
            },
            'timestamp': 1466585047605}

        return template

    @staticmethod
    def create_read():
        template = {
            'read': {
                'watermark': 1467892173172,
                'seq': 537
            },
            'timestamp': 1467892190179,
            'sender': {
                'id': '1129675700423442'
            },
            'recipient': {
                'id': '588667681307355'
            }
        }

        return template

    @staticmethod
    def create_not_supported():
        template = {
            'sender': {
                'id': 1
            },
            'not_supported': {
                'seq': 53,
                'mid': 'mid.1466750926480:b2598e311e5ad42d71',
                'text': 'text'
            },
            'recipient': {
                'id': 1
            },
            'timestamp': 1466750926487}

        return template
