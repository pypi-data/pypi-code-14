"""
Error Page

This plugin to display customize error page

Can be called as standalone
"""
from __future__ import division
import logging
from mambo import Mambo, page_meta, register_package, abort
from mambo import exceptions
from sqlalchemy.exc import SQLAlchemyError

register_package(__package__)

__version__ = "1.0.0"

# A callback function to use as renderer instead of the built in one
# A use case can be
renderer = None

"""
Example:

@render_as_json
def my_error(e):
    return {
        "error": True,
        "code": e.code,
        "message": e.description
    }, e.code
renderer = my_error
"""


def main(**kwargs):

    options = kwargs.get("options", {})
    template_page = options.get("template", "ErrorPage/index.html")

    class ErrorPage(Mambo):

        @classmethod
        def _register(cls, app, **kwargs):

            super(cls, cls)._register(app, **kwargs)

            @app.errorhandler(400)
            @app.errorhandler(401)
            @app.errorhandler(403)
            @app.errorhandler(404)
            @app.errorhandler(405)
            @app.errorhandler(406)
            @app.errorhandler(408)
            @app.errorhandler(409)
            @app.errorhandler(410)
            @app.errorhandler(413)
            @app.errorhandler(414)
            @app.errorhandler(429)
            @app.errorhandler(500)
            @app.errorhandler(501)
            @app.errorhandler(502)
            @app.errorhandler(503)
            @app.errorhandler(504)
            @app.errorhandler(505)
            def register_error(error):

                if isinstance(error, SQLAlchemyError):
                    error = SQLAlchemyHTTPException(error)

                # we'll log non 4** errors
                if int(error.code // 100) != 4:
                    _error = str(error)
                    _error += " - HTTException Code: %s" % error.code
                    _error += " - HTTException Description: %s" % error.description
                    logging.error(_error)

                if renderer:
                    return renderer(error)
                else:
                    page_meta(title="Error %s" % error.code)
                    return cls.render(error=error, _template=template_page), error.code

    return ErrorPage
