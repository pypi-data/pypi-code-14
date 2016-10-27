from .SMBase import SMBase

import smtplib
import email
import time

""" A class to send out emails.
"""

class Scan(SMBase):
"""Input:
    email: list of strings; emails to send results to.
"""

    def init(self, email, server='localhost'):
        """ Take in the email address(es)."""
        self.email = email
        self.server = server

    def send(self, message):
        """Send an email detailing the run."""
        if message = "":
            self.msg = email.mime.text.MimeText("An Empty result was passed \
                                                to Statmail Send")
            msg['Subject'] = "[StatMail] FAILED on" + time.strftime("%c")
            msg['To'] = ', '.join(email)
        else:
            # put message together
            self.msg = email.mime.text.MimeText(message)
            msg['Subject'] = "[StatMail] Scan on" + time.strftime("%c")
            msg['To'] = ', '.join(email)
        try:
            smtp = smtplib.SMTP(self.server)
            smtp.sendmail(self.email, msg.as_string())
        except:
            raise RuntimeError("Email send failed.")
