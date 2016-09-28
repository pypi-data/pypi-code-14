import logging

from ..rpc import BaseRPC
from ..exc import LoginRequired

log = logging.getLogger(__name__)


class RPC(BaseRPC):

    def check_op(self, op):
        if not self._auth and not op.get("request") == "Login":
            raise LoginRequired()

        if 'params' not in op:
            op['params'] = {}

        if 'version' not in op:
            if hasattr(self, 'version'):
                op['version'] = self.version
            else:
                raise KeyError('Operation is missing "Version": {}'.format(op))

        op['request-id'] = self._request_id
        self._request_id += 1
        return op

    def check_error(self, result):
        return result.get('error')

    def get_response(self, result):
        return result['response']

    def login_args(self, user, password):
        return {
            "type": "Admin",
            "request": "Login",
            "version": 3,
            "params": {"auth-tag": user,
                       "credentials": password}}
