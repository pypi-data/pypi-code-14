import json
from urllib import parse

import requests


class API:
    @staticmethod
    def get_test_api(flask_test_app, secret):
        return TestAPI(flask_test_app, secret)

    @staticmethod
    def get_http_api(end_point, secret):
        return HttpAPI(end_point, secret)

    # TODO: Make unregister_service()
    def register_service(self, service_id):
        res = self._post(201, '/metadata/services', {'service_id': service_id})
        return self.to_json(res)

    def list_services(self):
        res = self._get(200, '/metadata/services')
        return self.to_json(res)

    def update_config(self, service_id, config):
        res = self._put(200, '/metadata/services/%s' % service_id, config)
        return self.to_json(res)

    def get_config(self, service_id):
        res = self._get(200, '/metadata/services/%s' % service_id)
        return self.to_json(res)

    def flushall(self):
        res = self._post(200, '/metadata/flushall', {})
        return self.to_json(res)

    def route(self, service_id, exp_ids, tid, uid=None, forced_arm_ids=None):
        qs = {
            'exp_ids': ','.join(exp_ids),
            'tid': tid
        }
        if uid:
            qs['uid'] = uid
        if forced_arm_ids:
            qs['forced_arm_ids'] = json.dumps(forced_arm_ids)

        res = self._get(200, '/routes/%s' % service_id, qs)
        return self.to_json(res)

    def process_log(self, service_id, log):
        res = self._post(200, '/logs/%s' % service_id, log)
        return self.to_json(res)

    def report_all_arm_perfs(self, service_id):
        res = self._get(200, '/reports/%s' % service_id)
        return self.to_json(res)

    def report_arm_perfs(self, service_id, exp_id):
        res = self._get(200, '/reports/%s/%s' % (service_id, exp_id))
        return self.to_json(res)

    def report_arm_perf(self, service_id, exp_id, arm_id):
        res = self._get(200,
                        '/reports/%s/%s/%s' % (service_id, exp_id, arm_id))
        return self.to_json(res)

    def to_json(self, res):
        raise NotImplementedError

    def _get(self, expected_status, url, qs=None):
        raise NotImplementedError

    def _post(self, expected_status, url, data):
        raise NotImplementedError

    def _put(self, expected_status, url, data):
        raise NotImplementedError


class HttpAPI(API):
    def __init__(self, end_point, secret):
        self._end_point = end_point
        self._secret = secret

    def _post(self, expected_status, url, data):
        headers = {
            'content-type': 'application/json',
            'gbbox-secret': self._secret,
        }
        res = requests.post(self._end_point + url, data=json.dumps(data),
                            headers=headers)
        self._check_res(res, expected_status)
        return res

    def _put(self, expected_status, url, data):
        headers = {
            'content-type': 'application/json',
            'gbbox-secret': self._secret,
        }
        res = requests.put(self._end_point + url, data=json.dumps(data),
                           headers=headers)
        self._check_res(res, expected_status)
        return res

    def _get(self, expected_status, url, qs=None):
        headers = {
            'gbbox-secret': self._secret,
        }
        if qs is not None:
            url = url + '?' + parse.urlencode(qs)

        res = requests.get(self._end_point + url, headers=headers)
        self._check_res(res, expected_status)
        return res

    def to_json(self, res):
        return json.loads(res.text)

    def _check_res(self, res, expected_status):
        if res.status_code != expected_status:
            error = self.to_json(res)
            raise HttpRemoteError(
                res.status_code,
                error['error_type'],
                error['message'],
            )


class TestAPI(API):
    def __init__(self, flask_test_app, secret):
        self._app = flask_test_app
        self._secret = secret

    def _post(self, expected_status, url, data):
        headers = {
            'content-type': 'application/json',
            'gbbox-secret': self._secret,
        }
        res = self._app.post(url, data=json.dumps(data), headers=headers)
        self._check_res(res, expected_status)
        return res

    def _put(self, expected_status, url, data):
        headers = {
            'content-type': 'application/json',
            'gbbox-secret': self._secret,
        }
        res = self._app.put(url, data=json.dumps(data), headers=headers)
        self._check_res(res, expected_status)
        return res

    def _get(self, expected_status, url, qs=None):
        headers = {
            'gbbox-secret': self._secret,
        }
        if qs is not None:
            url = url + '?' + parse.urlencode(qs)

        res = self._app.get(url, headers=headers)
        self._check_res(res, expected_status)
        return res

    def to_json(self, res):
        return json.loads(res.data.decode('utf-8'))

    def _check_res(self, res, expected_status):
        if res.status_code != expected_status:
            error = self.to_json(res)
            raise HttpRemoteError(
                res.status_code,
                error['error_type'],
                error['message'],
            )


class HttpRemoteError(BaseException):
    def __init__(self, status_code, error_type, message):
        self._status_code = status_code
        self._error_type = error_type
        self._message = message

    @property
    def status_code(self):
        return self._status_code

    @property
    def error_type(self):
        return self._error_type

    @property
    def message(self):
        return self._message

    def __str__(self):
        return '%s: %s (%s)' % (
            self._error_type,
            self._message,
            self._status_code
        )


