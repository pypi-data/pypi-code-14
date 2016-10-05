#
# Copyright 2016 Formation Data Systems, Inc. All Rights Reserved.
#
from base_cli_test import BaseCliTest
from mock import patch
import mock_functions
from model.volume.volume import Volume
from utils.converters.volume.volume_converter import VolumeConverter

class VolumeListExportsTest( BaseCliTest ):
    '''
    Test case for listing exported volumes in a bucket. IS-A unittest.TestCase.
    '''
    @patch("services.volume_service.VolumeService.list_exports_in_bucket", side_effect=mock_functions.listExports)
    def test_list_exports(self, mockListExportsService):
        '''
        The volume service calls are replaced by mock functions.

        Parameters
        ----------
        mockListExportsService (unittest.mock.MagicMock)
        '''
        args = ["volume", "list_exports", "-s3_bucket_name=xvolrepo", "-s3_access_key=ABCDEFG",
            "-s3_secret_key=/52/yrwhere", "-url=https://s3.amazon.com"]

        self.callMessageFormatter(args)
        self.cli.run(args)
        assert mockListExportsService.call_count == 1

        repo = mockListExportsService.call_args[0][0]

        assert repo.url == "https://s3.amazon.com"
        assert repo.bucket_name == "xvolrepo"
        assert repo.remote_om == None
        assert repo.credentials.access_key_id == "ABCDEFG"
        assert repo.credentials.secret_key == "/52/yrwhere"

        print("test_list_exports passed.\n\n")

