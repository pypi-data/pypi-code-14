import json


class AuthInfoMiddleware(object):
    def process_template_response(self, request, response):
        if request.user.is_authenticated():
            user = request.user.username
        else:
            user = None
        is_admin = request.user.is_superuser
        response['x-authinfo'] = ';'.join([
            json.dumps(user),
            json.dumps(is_admin)
        ])
        return response
