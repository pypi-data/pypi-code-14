__version__ = '0.1'

import logging
import requests

class NinjaLogger(logging.Handler):
    """
    A class which sends records to a http://wwww.ninjalog.io
    """

    def __init__(self, email, client_id, client_secret,
        log_format='%(asctime)s %(levelname)s (%(pathname)s:%(lineno)d): %(message)s'):

        logging.Handler.__init__(self)

        self.headers = dict(
            Accept="application/json"
        )

        r = requests.post('http://www.ninjalog.io/api/v1/auth/token', json={
            'email' : email,
            'client_id' : client_id
        }, headers=self.headers)

        import jwt

        decoded = jwt.decode(r.text, client_secret)

        if decoded and decoded.has_key('auth_token'):
            self.headers.update(
                dict(Authorization="Bearer {0}".format(decoded['auth_token']))
            )

        self.setFormatter(logging.Formatter(log_format))

    def emit(self, record):
        """
        Emit a record.

        Send the record to the Web server as a percent-encoded dictionary
        """
        try:
            r = requests.post('http://www.ninjalog.io/api/v1/log', json={
                'message' : self.format(record)
            }, headers=self.headers)
        except:
            self.handleError(record)
