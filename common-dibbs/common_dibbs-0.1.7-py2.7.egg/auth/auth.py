from django.contrib.auth.models import User
from django.http import HttpResponse
from django.template import Template, Context
from django.template.loader import get_template, TemplateDoesNotExist

from django.shortcuts import redirect

from common_dibbs.config.configuration import Configuration
import base64
import requests


class ClientAuthenticationBackend(object):
    def authenticate(self, username=None, password=None, session_key=None):

        data = {
            "username": username,
            "password": password,
            "session_key": session_key,
        }

        result = None
        response = requests.post("%s/authenticate/" % (Configuration().get_central_authentication_service_url()), data=data)
        if response.status_code < 400:
            result = response.json()

        user = None
        if result and result["response"]:
            user = User()
            user.username = result["username"]

        return {
            "user": user,
            "token": result["token"]
        }

default_redirect_form_value = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Redirection to authentication server</title>
</head>
<body>
    <form id="redirect_form" action="{{ cas_service_target_url }}" method="POST">
        <input type="hidden" name="session_key" value="{{ session_key }}">
        <input type="hidden" name="redirect_url" value="{{ redirect_url }}">
        <button type="submit">You will be redirected to the authentication server</button>
    </form>
</body>
</html>
"""


class CentralAuthenticationMiddleware(object):
    def process_request(self, request):
        session_key = request.session.session_key
        username = None
        password = None

        if 'HTTP_AUTHORIZATION' in request.META and "Basic " in request.META.get('HTTP_AUTHORIZATION'):
            s = base64.b64decode(request.META.get('HTTP_AUTHORIZATION').split("Basic ")[1])
            username = s.split(":")[0]
            password = s.split(":")[1]
        auth_backend = ClientAuthenticationBackend()

        # Check if the current session has already been authenticated by the CAS: authentication is successful
        authentication_resp = auth_backend.authenticate(username, password, session_key)

        if authentication_resp["user"] is not None and authentication_resp["user"].username not in ["", "anonymous"]:
            request.user = authentication_resp["user"]
            return

        # Do a web redirection to the CAS service
        redirect_url = "http://%s%s" % (request.META.get('HTTP_HOST'), request.path)
        cas_service_target_url = "%s" % (Configuration().get_central_authentication_service_url(), )

        data = {
            "request": request,
            "session_key": session_key,
            "redirect_url": redirect_url,
            "cas_service_target_url": cas_service_target_url
        }

        try:
            t = get_template("redirect_form.html")
        except TemplateDoesNotExist:
            t = Template(default_redirect_form_value)

        c = Context(data)
        html_source = str(t.render(c))

        # Redirection via a form
        return HttpResponse(html_source)


def session_logout_view(request):

    session_key = request.session.session_key
    data = {
        "session_key": session_key,
    }

    result = None
    response = requests.post("%s/session_logout/" % (Configuration().get_central_authentication_service_url()), data=data)
    if response.status_code < 400:
        result = response.json()
    return redirect("/")


LOGGED_USERS = {

}
