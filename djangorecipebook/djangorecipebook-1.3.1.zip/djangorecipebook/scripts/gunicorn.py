from __future__ import absolute_import

import sys

try:
    from gunicorn.app.wsgiapp import run as gunicorn_run
except ImportError as e:
    # only there to tackle issues in Windows
    def gunicorn_run():
        if sys.platform == 'win32':
            raise RuntimeError(
                'djangorecipebook:gunicorn is not available on Windows because'
                'gunicorn can only work on UNIX platforms'
            )
        else:
            raise e


def main(application):
    if application:
        sys.argv.append(application)
    gunicorn_run()
