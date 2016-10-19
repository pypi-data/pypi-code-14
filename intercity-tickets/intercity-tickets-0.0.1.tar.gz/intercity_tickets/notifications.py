import os

import dj_email_url
import emails


class EmailNotification(object):

    def __init__(self, email_url, receiver):
        self.config = dj_email_url.config(default=email_url)
        self.receiver = receiver

    def notify(self, ticket, attachment=None):
        subject = '%s - Wagon %s, miejsce %s (%s), %s' % (
            ticket.date.strftime('%H:%M'),
            ticket.carriage, ticket.seat, ticket.location, ticket.carriage_type)
        message = emails.html(
            html='%s, %s - %s' % (
                ticket.date.strftime('%A, %d %b'),
                ticket.route_from,
                ticket.route_to),
            subject=subject,
            mail_from=('Tickets', self.config['EMAIL_HOST_USER']))
        if attachment:
            filename = os.path.basename(attachment.name)
            message.attach(data=attachment, filename=filename)
        message.send(to=self.receiver, smtp={
            'host': self.config['EMAIL_HOST'],
            'port': self.config['EMAIL_PORT'],
            'ssl': self.config['EMAIL_USE_TLS'],
            'user': self.config['EMAIL_HOST_USER'],
            'password': self.config['EMAIL_HOST_PASSWORD']})
