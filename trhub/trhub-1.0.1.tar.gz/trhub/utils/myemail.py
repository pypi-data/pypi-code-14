from email.message import Message
from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class myemail:
    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password
        self.sm = SMTP(host=self.host)
        self.sm.login(self.username, self.password)

    def send(self, title, html, to):
        msgAlternative = MIMEMultipart('alternative')
        msg = MIMEText(
            "<html><head><style>table {width: 100%}th, td {border: 1px solid #000000;text-align: center;}</style></head><body>" + html + "</body></html>",
            'html', _charset="utf-8")
        msgAlternative["Subject"] = title
        msgAlternative["From"] = self.username
        if type(to) is not list:
            to = [to]
        msg["To"] = ",".join(to)
        msgAlternative.attach(msg)
        # msg.set_payload(html)
        self.sm.sendmail(self.username, to, msgAlternative.as_string())
