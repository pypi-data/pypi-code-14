# Copyright 2016 Formation Data Systems, Inc. All Rights Reserved.
#
from base_cli_test import BaseCliTest
from mock import patch
import mock_functions
from model.common.named_credential import NamedCredential
from model.common.s3credentials import S3Credentials
from model.volume.volume import Volume
from utils.converters.volume.volume_converter import VolumeConverter

def mockGetNamedCredential(key):
    credential = NamedCredential()
    credential.s3credentials = S3Credentials()
    credential.bucketname = "xvolrepo"
    credential.s3credentials.access_key_id = "ABCDEFG"
    credential.s3credentials.secret_key = "/52/yrwhere"
    credential.url = "https://s3.amazon.com"
    return credential

class TestExportsList( BaseCliTest ):
    '''
    Test case for listing exported volumes in a bucket. IS-A unittest.TestCase.
    '''
    @patch("services.subscription.named_credential_client.NamedCredentialClient.get_named_credential_by_key",
        side_effect=mockGetNamedCredential)
    @patch("services.volume_service.VolumeService.list_exports_in_bucket", side_effect=mock_functions.listExports)
    def test_list_exports(self, mockListExportsService, mockGetNamedCredential):
        '''
        The volume service calls are replaced by mock functions.

        Parameters
        ----------
        mockListExportsService (unittest.mock.MagicMock)
        mockGetNamedCredential (unittest.mock.MagicMock)
        '''
        args = ["exports", "list", "-s3_access_key=ABCDEFG", "-s3_secret_key=/52/yrwhere",
            "-url=https://s3.amazon.com", "xvolrepo"]

        self.callMessageFormatter(args)
        self.cli.run(args)
        assert mockListExportsService.call_count == 1

        repo = mockListExportsService.call_args[0][0]

        assert repo.url == "https://s3.amazon.com"
        assert repo.bucket_name == "xvolrepo"
        assert repo.remote_om == None
        assert repo.credentials.access_key_id == "ABCDEFG"
        assert repo.credentials.secret_key == "/52/yrwhere"

        # Again, using a named credential
        args = ["exports", "list", "-c=cred"]

        self.callMessageFormatter(args)
        self.cli.run(args)
        assert mockListExportsService.call_count == 2
        assert mockGetNamedCredential.call_count == 1

        repo = mockListExportsService.call_args[0][0]

        assert repo.url == "https://s3.amazon.com"
        assert repo.bucket_name == "xvolrepo"
        assert repo.remote_om == None
        assert repo.credentials.access_key_id == "ABCDEFG"
        assert repo.credentials.secret_key == "/52/yrwhere"

        print("test_list_exports passed.\n\n")

