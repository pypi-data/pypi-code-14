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

    def __init__(self, end_point, req, secret):
        self._end_point = end_point
        self._req = req
        self._secret = secret

    def register_service(self, service_id):
        res = self._post(201, '/metadata/services', {'service_id': service_id})
        return self._to_json(res)

    def unregister_service(self, service_id):
        res = self._delete(200, '/metadata/services/%s' % service_id)
        return self._to_json(res)

    def list_services(self):
        res = self._get(200, '/metadata/services')
        return self._to_json(res)

    def update_config(self, service_id, config):
        res = self._put(200, '/metadata/services/%s' % service_id, config)
        return self._to_json(res)

    def get_config(self, service_id):
        res = self._get(200, '/metadata/services/%s' % service_id)
        return self._to_json(res)

    def flushall(self):
        res = self._post(200, '/metadata/flushall', {})
        return self._to_json(res)

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
        return self._to_json(res)

    def process_log(self, service_id, log):
        res = self._post(200, '/logs/%s' % service_id, log)
        return self._to_json(res)

    def report_all_arm_perfs(self, service_id):
        res = self._get(200, '/reports/%s' % service_id)
        return self._to_json(res)

    def report_arm_perfs(self, service_id, exp_id):
        res = self._get(200, '/reports/%s/%s' % (service_id, exp_id))
        return self._to_json(res)

    def report_arm_perf(self, service_id, exp_id, arm_id):
        res = self._get(200,
                        '/reports/%s/%s/%s' % (service_id, exp_id, arm_id))
        return self._to_json(res)

    def _get(self, expected_status, url, qs=None):
        headers, full_url = self._build_req(url, qs)
        res = self._req.get(full_url, headers=headers)
        self._check_res(res, expected_status)
        return res

    def _put(self, expected_status, url, data, qs=None):
        headers, full_url = self._build_req(url, qs)
        res = self._req.put(full_url, data=json.dumps(data), headers=headers)
        self._check_res(res, expected_status)
        return res

    def _post(self, expected_status, url, data, qs=None):
        headers, full_url = self._build_req(url, qs)
        res = self._req.post(full_url, data=json.dumps(data), headers=headers)
        self._check_res(res, expected_status)
        return res

    def _delete(self, expected_status, url, qs=None):
        headers, full_url = self._build_req(url, qs)
        res = self._req.delete(full_url, headers=headers)
        self._check_res(res, expected_status)
        return res

    def _build_req(self, url, qs):
        headers = {
            'content-type': 'application/json',
            'gbbox-secret': self._secret,
        }
        if qs is not None:
            url = url + '?' + parse.urlencode(qs)

        return headers, url

    def _to_json(self, res):
        raise NotImplementedError

    def _check_res(self, res, expected_status):
        if res.status_code != expected_status:
            error = self._to_json(res)
            raise HttpRemoteError(
                res.status_code,
                error['error_type'],
                error['message'],
            )


class HttpAPI(API):
    def __init__(self, end_point, secret):
        super().__init__(end_point, requests, secret)

    def _to_json(self, res):
        return json.loads(res.text)


class TestAPI(API):
    def __init__(self, flask_test_app, secret):
        super().__init__('', flask_test_app, secret)

    def _to_json(self, res):
        return json.loads(res.data.decode('utf-8'))


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
