# Copyright 2016 Formation Data Systems, Inc. All Rights Reserved.
#
from base_cli_test import BaseCliTest
from mock import patch
import mock_functions
from model.common.named_credential import NamedCredential
from model.common.s3credentials import S3Credentials
from model.volume.volume import Volume
from utils.converters.volume.volume_converter import VolumeConverter

def mock_create(named_credential):
    return named_credential

class TestCredentialSave(BaseCliTest):
    '''Tests plugin and service client functionality for ``credential save`` commands.

    IS-A unittest.TestCase.
    '''
    @patch("services.subscription.named_credential_client.NamedCredentialClient.create_named_credential",
        side_effect=mock_create)
    @patch("services.subscription.named_credential_client.NamedCredentialClient.get_named_credentials",
        side_effect=mock_functions.empty)
    def test_save_f1(self, mockGet, mockCreate):
        '''Tests the credential plugin for ``credential save f1``.

        A parser for the command is created in the NamedCredentialPlugin.
        All service client calls are mocked.

        Parameters
        ----------
        :type mockGet: ``unittest.mock.MagicMock``
        :type mockCreate: ``unittest.mock.MagicMock``
        '''
        print("Plugin test: credential save f1")

        args = ["credential", "save", "f1", "credentialNameF1", "https", "hannah.reid", "secret",
            "localhost", "7777"]

        self.callMessageFormatter(args)
        self.cli.run(args)
        assert mockCreate.call_count == 1
        assert mockGet.call_count == 1

        credential = mockCreate.call_args[0][0]

        assert credential.hostname == "localhost"
        assert credential.name == "credentialNameF1"
        assert credential.url == "https://hannah.reid:secret@localhost:7777"
        assert credential.bucketname == None
        assert credential.password == "secret"
        assert credential.port == 7777
        assert credential.username == "hannah.reid"

        print("PASSED.\n")

    @patch("services.subscription.named_credential_client.NamedCredentialClient.create_named_credential",
        side_effect=mock_create)
    @patch("services.subscription.named_credential_client.NamedCredentialClient.get_named_credentials",
        side_effect=mock_functions.empty)
    def test_save_s3(self, mockGet, mockCreate):
        '''Tests the credential plugin for ``credential save s3``.

        A parser for the command is created in the NamedCredentialPlugin.
        All service client calls are mocked.

        Parameters
        ----------
        :type mockGet: ``unittest.mock.MagicMock``
        :type mockCreate: ``unittest.mock.MagicMock``
        '''
        print("Plugin test: credential save s3")

        args = ["credential", "save", "s3", "credentialNameS3", "https://s3.amazon.com",
            "xvolrepo", "ABCDEFG", "/52/yrwhere"]

        self.callMessageFormatter(args)
        self.cli.run(args)
        assert mockCreate.call_count == 1
        assert mockGet.call_count == 1

        credential = mockCreate.call_args[0][0]

        assert credential.name == "credentialNameS3"
        assert credential.url == "https://s3.amazon.com"
        assert credential.bucketname == "xvolrepo"
        assert credential.s3credentials.access_key_id == "ABCDEFG"
        assert credential.s3credentials.secret_key == "/52/yrwhere"

        print("PASSED.\n")

