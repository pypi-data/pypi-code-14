import json
import unittest
import urllib.parse
from unittest.mock import Mock, MagicMock

from gbboxcli.api import API, HttpRemoteError


class APITest(unittest.TestCase):
    def setUp(self):
        self._expected_headers = {'gbbox-secret': 'SECRET',
                                  'content-type': 'application/json'}
        self._expected_req_body = {'A': 'B'}
        self._expected_res_body = {'C': 'D'}
        self._expected_error = {'error_type': 'E', 'message': 'M'}

    def test_register_service(self):
        mock_req = self.build_post(201, self._expected_res_body)
        api = self.build_api(mock_req)

        res = api.register_service('goog')

        self.assertDictEqual(self._expected_res_body, res)
        mock_req.post.assert_called_with(
            '/metadata/services',
            data=json.dumps({'service_id': 'goog'}),
            headers=self._expected_headers,
        )

    def test_register_service_with_error(self):
        mock_req = self.build_post(400, self._expected_error)
        api = self.build_api(mock_req)

        with self.assertRaises(HttpRemoteError) as ctx:
            api.register_service('goog')
        self.assertRemoteError(ctx.exception)

    def test_unregister_service(self):
        mock_req = self.build_delete(200, self._expected_res_body)
        api = self.build_api(mock_req)

        res = api.unregister_service('goog')

        self.assertDictEqual(self._expected_res_body, res)
        mock_req.delete.assert_called_with(
            '/metadata/services/goog',
            headers=self._expected_headers,
        )

    def test_unregister_service_with_error(self):
        mock_req = self.build_delete(400, self._expected_error)
        api = self.build_api(mock_req)

        with self.assertRaises(HttpRemoteError) as ctx:
            api.unregister_service('goog')
        self.assertRemoteError(ctx.exception)

    def test_list_services(self):
        mock_req = self.build_get(200, self._expected_res_body)
        api = self.build_api(mock_req)

        res = api.list_services()

        self.assertDictEqual(self._expected_res_body, res)
        mock_req.get.assert_called_with(
            '/metadata/services',
            headers=self._expected_headers,
        )

    def test_list_services_with_error(self):
        mock_req = self.build_get(400, self._expected_error)
        api = self.build_api(mock_req)

        with self.assertRaises(HttpRemoteError) as ctx:
            api.list_services()
        self.assertRemoteError(ctx.exception)

    def test_update_config(self):
        mock_req = self.build_put(200, self._expected_res_body)
        api = self.build_api(mock_req)

        res = api.update_config('goog', self._expected_req_body)

        self.assertDictEqual(self._expected_res_body, res)
        mock_req.put.assert_called_with(
            '/metadata/services/goog',
            data=json.dumps(self._expected_req_body),
            headers=self._expected_headers,
        )

    def test_unpdate_config_with_error(self):
        mock_req = self.build_put(400, self._expected_error)
        api = self.build_api(mock_req)

        with self.assertRaises(HttpRemoteError) as ctx:
            api.update_config('goog', self._expected_req_body)
        self.assertRemoteError(ctx.exception)

    def test_get_config(self):
        mock_req = self.build_get(200, self._expected_res_body)
        api = self.build_api(mock_req)

        res = api.get_config('goog')

        self.assertDictEqual(self._expected_res_body, res)
        mock_req.get.assert_called_with(
            '/metadata/services/goog',
            headers=self._expected_headers,
        )

    def test_get_config_with_error(self):
        mock_req = self.build_get(400, self._expected_error)
        api = self.build_api(mock_req)

        with self.assertRaises(HttpRemoteError) as ctx:
            api.get_config('goog')
        self.assertRemoteError(ctx.exception)

    def test_flushall(self):
        mock_req = self.build_post(200, self._expected_res_body)
        api = self.build_api(mock_req)

        res = api.flushall()

        self.assertDictEqual(self._expected_res_body, res)
        mock_req.post.assert_called_with(
            '/metadata/flushall',
            data=json.dumps({}),
            headers=self._expected_headers,
        )

    def test_flushall_with_error(self):
        mock_req = self.build_post(400, self._expected_error)
        api = self.build_api(mock_req)

        with self.assertRaises(HttpRemoteError) as ctx:
            api.flushall()
        self.assertRemoteError(ctx.exception)

    def test_route_with_uid_forced_arm_ids(self):
        mock_req = self.build_get(200, self._expected_res_body)
        api = self.build_api(mock_req)

        res = api.route('goog', ['e1', 'e2'], 'TID', 'UID', {'e1': 'v1/a'})

        self.assertDictEqual(self._expected_res_body, res)

        actual_path, qs = mock_req.get.call_args[0][0].split('?')
        actual_headers = mock_req.get.call_args[1]['headers']

        expected_path = '/routes/goog'
        self.assertEqual(expected_path, actual_path)

        self.assertDictEqual(self._expected_headers, actual_headers)

        expected_qs = {
            'uid': 'UID',
            'exp_ids': 'e1,e2',
            'forced_arm_ids': '{"e1": "v1/a"}',
            'tid': 'TID'
        }
        actual_qs = dict(urllib.parse.parse_qsl(qs))
        self.assertDictEqual(expected_qs, actual_qs)

    def test_route_without_uid_forced_arm_ids(self):
        mock_req = self.build_get(200, self._expected_res_body)
        api = self.build_api(mock_req)

        res = api.route('goog', ['e1', 'e2'], 'TID')

        self.assertDictEqual(self._expected_res_body, res)

        actual_path, qs = mock_req.get.call_args[0][0].split('?')
        actual_headers = mock_req.get.call_args[1]['headers']

        expected_path = '/routes/goog'
        self.assertEqual(expected_path, actual_path)

        self.assertDictEqual(self._expected_headers, actual_headers)

        expected_qs = {
            'tid': 'TID',
            'exp_ids': 'e1,e2',
        }
        actual_qs = dict(urllib.parse.parse_qsl(qs))
        self.assertDictEqual(expected_qs, actual_qs)

    def test_route_with_error(self):
        mock_req = self.build_get(400, self._expected_error)
        api = self.build_api(mock_req)

        with self.assertRaises(HttpRemoteError) as ctx:
            api.route('goog', ['e1', 'e2'], 'TID')
        self.assertRemoteError(ctx.exception)

    def test_process_log(self):
        mock_req = self.build_post(200, self._expected_res_body)
        api = self.build_api(mock_req)

        res = api.process_log('goog', self._expected_req_body)

        self.assertDictEqual(self._expected_res_body, res)
        mock_req.post.assert_called_with(
            '/logs/goog',
            data=json.dumps(self._expected_req_body),
            headers=self._expected_headers,
        )

    def test_process_log_with_error(self):
        mock_req = self.build_post(400, self._expected_error)
        api = self.build_api(mock_req)

        with self.assertRaises(HttpRemoteError) as ctx:
            api.process_log('goog', self._expected_req_body)
        self.assertRemoteError(ctx.exception)

    def test_report_all_arm_perfs(self):
        mock_req = self.build_get(200, self._expected_res_body)
        api = self.build_api(mock_req)

        res = api.report_all_arm_perfs('goog')

        self.assertDictEqual(self._expected_res_body, res)
        mock_req.get.assert_called_with(
            '/reports/goog',
            headers=self._expected_headers,
        )

    def test_report_all_arm_perfs_with_error(self):
        mock_req = self.build_get(400, self._expected_error)
        api = self.build_api(mock_req)

        with self.assertRaises(HttpRemoteError) as ctx:
            api.report_all_arm_perfs('goog')
        self.assertRemoteError(ctx.exception)

    def test_report_arm_perfs(self):
        mock_req = self.build_get(200, self._expected_res_body)
        api = self.build_api(mock_req)

        res = api.report_arm_perfs('goog', 'exp1')

        self.assertDictEqual(self._expected_res_body, res)
        mock_req.get.assert_called_with(
            '/reports/goog/exp1',
            headers=self._expected_headers,
        )

    def test_report_arm_perfs_with_error(self):
        mock_req = self.build_get(400, self._expected_error)
        api = self.build_api(mock_req)

        with self.assertRaises(HttpRemoteError) as ctx:
            api.report_arm_perfs('goog', 'exp1')
        self.assertRemoteError(ctx.exception)

    def test_report_arm_perf(self):
        mock_req = self.build_get(200, self._expected_res_body)
        api = self.build_api(mock_req)

        res = api.report_arm_perf('goog', 'exp1', 'var1/a')

        self.assertDictEqual(self._expected_res_body, res)
        mock_req.get.assert_called_with(
            '/reports/goog/exp1/var1/a',
            headers=self._expected_headers,
        )

    def test_report_arm_perf_with_error(self):
        mock_req = self.build_get(400, self._expected_error)
        api = self.build_api(mock_req)

        with self.assertRaises(HttpRemoteError) as ctx:
            api.report_arm_perf('goog', 'exp1', 'var1/a')
        self.assertRemoteError(ctx.exception)

    @staticmethod
    def build_api(req):
        return API.get_test_api(req, 'SECRET')

    @staticmethod
    def build_get(res_status_code, res_body):
        mock_req = MagicMock()
        mock_res = MagicMock()
        mock_res.status_code = res_status_code
        mock_res.data = json.dumps(res_body).encode('utf-8')
        mock_req.get = Mock(return_value=mock_res)
        return mock_req

    @staticmethod
    def build_put(res_status_code, res_body):
        mock_req = MagicMock()
        mock_res = MagicMock()
        mock_res.status_code = res_status_code
        mock_res.data = json.dumps(res_body).encode('utf-8')
        mock_req.put = Mock(return_value=mock_res)
        return mock_req

    @staticmethod
    def build_post(res_status_code, res_body):
        mock_req = MagicMock()
        mock_res = MagicMock()
        mock_res.status_code = res_status_code
        mock_res.data = json.dumps(res_body).encode('utf-8')
        mock_req.post = Mock(return_value=mock_res)
        return mock_req

    @staticmethod
    def build_delete(res_status_code, res_body):
        mock_req = MagicMock()
        mock_res = MagicMock()
        mock_res.status_code = res_status_code
        mock_res.data = json.dumps(res_body).encode('utf-8')
        mock_req.delete = Mock(return_value=mock_res)
        return mock_req

    def assertRemoteError(self, err):
        self.assertEqual('M', err.message)
        self.assertEqual('E', err.error_type)


if __name__ == '__main__':
    unittest.main()
