import os
from unittest import TestCase
from moto import mock_s3

from gbdx_cloud_harness.services.account_storage_service import AccountStorageService


class TestPortService(TestCase):

    def setUp(self):
        self.mock = mock_s3()
        self.mock.start()

        self.test_bucket = 'bckt_not_provided'
        self.test_account_id = 'pre_not_provided'

        self.test_storage = AccountStorageService(is_test=True)

    def tearDown(self):
        self.mock.stop()

    def test_location(self):
        loc_path = self.test_storage.location
        assert self.test_bucket in loc_path
        assert self.test_account_id in loc_path

    def test_upload_file(self):
        upload_file = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'input', 'app.py'
        )
        s3_path = 'input/app.py'
        self.test_storage.upload((upload_file, s3_path))

        bucket_contents = self.test_storage.client.list_objects(Bucket=self.test_bucket)['Contents']

        assert bucket_contents[0]['Key'] == '%s/%s' % (self.test_account_id, s3_path)

        acct_contents = self.test_storage.list()

        assert acct_contents[0] == '%s/%s' % (self.test_account_id, s3_path)

        upload_file = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'input', 'app.py'
        )
        self.test_storage.upload((upload_file, 'app.py'))

        acct_contents = self.test_storage.list()
        acct_contents_input = self.test_storage.list(s3_folder='input')

        # assert only one file was listed.
        assert len(acct_contents) == 2
        assert acct_contents_input[0] == '%s/%s' % (self.test_account_id, s3_path)