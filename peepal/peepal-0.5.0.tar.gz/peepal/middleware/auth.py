from urllib.parse import urlencode
import re
from ..web import HttpError, logger

# patch_vary_headers is copied from django
cc_delim_re = re.compile(r'\s*,\s*')


def patch_vary_headers(response, newheaders):
    """
    Adds (or updates) the "Vary" header in the given HttpResponse object.
    newheaders is a list of header names that should be in "Vary". Existing
    headers in "Vary" aren't removed.
    """
    # Note that we need to keep the original order intact, because cache
    # implementations may rely on the order of the Vary contents in, say,
    # computing an MD5 hash.
    if 'Vary' in response.headers:
        vary_headers = cc_delim_re.split(response['Vary'])
    else:
        vary_headers = []
    # Use .lower() here so we treat headers as case-insensitive.
    existing_headers = set(header.lower() for header in vary_headers)
    additional_headers = [newheader for newheader in newheaders
                          if newheader.lower() not in existing_headers]
    response.headers['Vary'] = ', '.join(vary_headers + additional_headers)


class Authenticate:
    def __init__(self, user_getter, cookie_name='user'):
        self.user_getter = user_getter
        self.cookie_name = cookie_name

    def __call__(self, controller, next):
        request = controller.request
        token = request.get_cookie(self.cookie_name)
        request.user = self.user_getter(token) if token else None
        try:
            next()
        finally:
            patch_vary_headers(controller.response, ('Cookie',))


class LoginRequired:
    def __init__(self, login_url='/users/login', redirect_field_name='next'):
        self.login_url = login_url
        self.redirect_field_name = redirect_field_name

    def __call__(self, controller, next):
        request = controller.request
        if request.user:
            next()
        else:
            if request.is_ajax:
                raise HttpError(401)
            url = self.login_url + "?" + urlencode({self.redirect_field_name: request.url}, safe='/')
            controller.redirect_to_url(url)


class RolesRequired:
    def __init__(self, roles):
        self.roles = roles

    def __call__(self, controller, next):
        request = controller.request
        roles = request.user.roles
        if not self.roles or any(role in roles for role in self.roles):
            next()
        else:
            logger.debug('{}: require any of role(s) {}, user role(s) are {}'.format(controller.request.path, self.roles, roles))
            raise HttpError(403)
