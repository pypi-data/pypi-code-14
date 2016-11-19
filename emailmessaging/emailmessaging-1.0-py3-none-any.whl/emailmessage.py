import envelopes


class EmailMessage:
    def __init__(self, sender, receiver, subject, message, attachments=None):
        if not attachments:
            attachments = []

        envelope_options = {
            'from_addr': sender,
            'to_addr': receiver,
            'subject': subject,
            'html_body': message,
        }

        self.envelope = envelopes.Envelope(**envelope_options)

        for attachment in attachments:
            self.envelope.add_attachment(attachment)

        self.sender = sender

    def send(self, password, sender=None, server='smtp.googlemail.com', tls=True):
        if not sender:
            sender = self.sender
        self.envelope.send(host=server, login=sender, password=password, tls=tls)
