import json
import os
import requests
import six
import unittest

from mock import Mock, patch

from applause import settings
from applause.ais import (
    ApplauseAIS, filename_to_platform, InvalidCustomerKeyError, InvalidAppKeyError, ProcessingState,
    AIS_SETTINGS)


curr_dir = os.path.dirname(os.path.abspath(__file__))
test_app_path = os.path.join(curr_dir, os.path.pardir, os.path.pardir, 'test_files', 'Test.ipa')


class ApplauseAISTest(unittest.TestCase):

    def setUp(self):
        self.customer_key = 1
        self.session_mock = Mock()
        self.ais = ApplauseAIS(self.session_mock, customer_key=self.customer_key)
        self.ais.platform = 'ios'

    @patch('applause.ais.ApplauseAIS.run_instrument')
    def test_process_exects_run_instrument(self, run_instrument):
        input_file = six.StringIO()
        output_file = six.StringIO()
        self.ais.process(input_file=input_file, app_key='X', output_file=output_file)
        run_instrument.assert_called_once_with(input_file=input_file, app_key='X', output_file=output_file)

    @patch('time.sleep')  # to seed up tests
    @patch('applause.ais.ApplauseAIS.upload')
    @patch('applause.ais.ApplauseAIS.schedule')
    @patch('applause.ais.ApplauseAIS.poll_status')
    @patch('applause.utils.download')
    def test_run_instrument(self, download, poll_status, schedule, upload, _):
        upload.return_value = ('http://test.zip', 'data')
        schedule.return_value = ('token', 'data')
        poll_status.return_value = [('done', {'processed_url': 'http://test-out.zip'})]
        download.return_value = []

        input_file = six.StringIO()
        output_file = six.StringIO()
        self.ais.run_instrument(input_file=input_file, app_key='X', output_file=output_file)

        upload.assert_called_once_with(input_file)
        schedule.assert_called_once_with('X', 'ios', 'http://test.zip')
        poll_status.assert_called_once_with('token', max_tries=30)
        download.assert_called_once_with('http://test-out.zip', output_file, chunk_size=1024 * 1024)

    def test_process_invalid_customer_key(self):
        response = Mock()
        response.status_code = 401
        exc = requests.exceptions.HTTPError(response=response)

        input_file = six.StringIO()
        output_file = six.StringIO()

        with patch('applause.ais.ApplauseAIS.run_instrument', side_effect=exc) as run_instrument:
            self.assertRaises(InvalidCustomerKeyError, self.ais.process, input_file, '1', output_file)

        run_instrument.assert_called_once_with(input_file, '1', output_file)

    @patch('requests.post')
    @patch('applause.ais.ApplauseAIS._get_upload_data')
    def test_upload(self, get_upload_data, post):
        upload_data = {
            'action': 'store',
            'fields': {},
            'upload_url': 'https://test.zip'
        }
        get_upload_data.return_value = upload_data

        input_file = six.StringIO('some content')

        response = requests.Response()
        response.status_code = 200
        response._content = bytes(''.encode('utf-8'))

        post.return_value = response
        output = self.ais.upload(input_file)

        assert output == ('https://test.zip', upload_data)

    def test_schedule(self):
        response = requests.Response()
        response.status_code = 200
        response._content = bytes(json.dumps({'token': 'job-XYZ-scheduled'}).encode('utf-8'))

        with patch.object(self.ais.session, 'post') as post:
            post.return_value = response
            output = self.ais.schedule(app_key='X', platform='Xamarin', build_url='https://test.zip')

        # Output is a tuple of status & response data
        data = {
            'app_url': 'https://test.zip',
            'platform': 'Xamarin',
            'app_key': 'X',
            'server_url': settings.MBM_ROOT_URL.rstrip('/'),
        }
        data.update(AIS_SETTINGS)
        post.assert_called_once_with(settings.AIS_INSTRUMENT_URL, data=data, params={'apikey': self.customer_key})
        assert len(output) == 2
        assert output[0] == 'job-XYZ-scheduled'
        assert output[1] == {'token': 'job-XYZ-scheduled'}

    def test_schedule_invalid_app_key(self):
        response = Mock()
        response.status_code = 400

        with patch.object(self.ais.session, 'post') as post:
            post.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError(response=response)
            self.assertRaises(InvalidAppKeyError, self.ais.schedule, 'key', 'ios', 'http://dummy.com')

    def test_get_status(self):
        response = requests.Response()
        response.status_code = 200
        response._content = bytes(json.dumps({'status': 'foo'}).encode('utf-8'))

        with patch.object(self.ais.session, 'get') as get:
            get.return_value = response
            output = self.ais.get_status('token')

        # Output is a tuple of status & response data
        assert len(output) == 2
        assert output[0] == 'foo'
        assert output[1] == {'status': 'foo'}

    def test_poll_status_default_num_iterations(self):
        token = "<token>"
        with patch('applause.ais.ApplauseAIS.get_status') as get_status:
            get_status.return_value = (ProcessingState.pending.name, '<data>')
            list(self.ais.poll_status(token))

        get_status.assert_called_once_with(token)

    def test_repeat_poll_status_always_pending(self):
        token = "<token>"
        with patch('applause.ais.ApplauseAIS.get_status') as get_status:
            get_status.return_value = (ProcessingState.pending.name, '<data>')
            list(self.ais.poll_status(token, 10))

        assert get_status.call_count == 10

    def test_quit_poll_status_on_success(self):
        token = "<token>"
        with patch('applause.ais.ApplauseAIS.get_status') as get_status:
            get_status.return_value = (ProcessingState.success.name, '<data>')
            list(self.ais.poll_status(token, 10))

        assert get_status.call_count == 1

    def test_quit_poll_status_on_error(self):
        token = "<token>"
        with patch('applause.ais.ApplauseAIS.get_status') as get_status:
            get_status.return_value = (ProcessingState.error.name, '<data>')
            list(self.ais.poll_status(token, 10))

        assert get_status.call_count == 1

    def test_filename_to_extesion_ipa(self):
        assert filename_to_platform('test.ipa') == ('ios', 'ipa')

    def test_filename_to_extesion_apk(self):
        assert filename_to_platform('test.apk') == ('android', 'apk')

    def test_filename_to_extesion_illegal(self):
        self.assertRaises(ValueError, filename_to_platform, 'test.xyz')
