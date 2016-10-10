import os
from flask_error import default_error
from flask import make_response
import jinja2



def FlaskError(app, custom_error_page=None):

    if custom_error_page:
        ERR_TEMPLATE = custom_error_page

    else:
        extra_folders = jinja2.ChoiceLoader([
            app.jinja_loader,
            jinja2.FileSystemLoader(os.path.dirname(default_error.__file__)),
        ])
        app.jinja_loader = extra_folders
        ERR_TEMPLATE = 'error.html'

    @app.errorhandler(Exception)
    def handle_error(e):
        if isinstance(e, HTTPException):
            public_message = e.code
        elif isinstance(e, PublicErrorMessage):
            public_message = 'yes'

        return make_response(ERR_TEMPLATE, 
                             title='Error', 
                             public_message=public_message)

class PublicErrorMessage(Exception):
    def __init__(self, http_status_code, public_message):
        Exception.__init__(self)
        self.public_message = public_message
        self.http_status_code = http_status_code
