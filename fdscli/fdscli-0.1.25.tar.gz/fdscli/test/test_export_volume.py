#
# Copyright 2016 Formation Data Systems, Inc. All Rights Reserved.
#
from base_cli_test import BaseCliTest
from mock import patch
import mock_functions
from model.common.repository import Repository
from model.volume.volume import Volume
from services.fds_auth import FdsAuth
from services.volume_service import VolumeService
from utils.converters.common.repository_converter import RepositoryConverter
from utils.converters.volume.volume_converter import VolumeConverter

def mock_post( session, url, data ):
    print url

def mock_get_url_preamble():
    return "http://localhost:7777/fds/config/v09"

class VolumeExportTest( BaseCliTest ):
    '''
    Test case for volume export. IS-A unittest.TestCase.
    '''
    @patch("plugins.volume_plugin.VolumePlugin.pretty_print_volume", side_effect=mock_functions.empty_one)
    @patch("services.response_writer.ResponseWriter.writeTabularData", side_effect=mock_functions.empty_one)
    @patch("services.volume_service.VolumeService.export_volume", side_effect=mock_functions.exportVolume)
    @patch("services.volume_service.VolumeService.get_volume", side_effect=mock_functions.getVolume)
    def test_export_volume(self, mockGetVolume, mockExportVolume, mockTabular, mockPretty):
        '''
        The volume service calls are replaced by mock functions.

        Parameters
        ----------
        mockGetVolume (unittest.mock.MagicMock)
        mockExportVolume (unittest.mock.MagicMock)
        mockTabular (unittest.mock.MagicMock)
        mockPretty (unittest.mock.MagicMock)
        '''
        args = ["volume", "export", "-volume_id=3", "-s3_bucket_name=xvolrepo", "-s3_access_key=ABCDEFG",
            "-s3_secret_key=/52/yrwhere", "-url=https://s3.amazon.com"]

        self.callMessageFormatter(args)
        self.cli.run(args)
        assert mockExportVolume.call_count == 1

        volume = mockExportVolume.call_args[0][0]

        assert volume.id == 3

        repo = mockExportVolume.call_args[0][1]

        j_repo = RepositoryConverter.to_json(repo)
        print j_repo

        assert repo.url == "https://s3.amazon.com"
        assert repo.bucket_name == "xvolrepo"
        assert repo.remote_om == None
        assert repo.credentials.access_key_id == "ABCDEFG"
        assert repo.credentials.secret_key == "/52/yrwhere"

        print("test_export_volume passed.\n\n")

    @patch("plugins.volume_plugin.VolumePlugin.pretty_print_volume", side_effect=mock_functions.empty_one)
    @patch("services.response_writer.ResponseWriter.writeTabularData", side_effect=mock_functions.empty_one)
    @patch("services.volume_service.VolumeService.export_volume", side_effect=mock_functions.exportVolume)
    @patch("services.volume_service.VolumeService.get_volume", side_effect=mock_functions.getVolume)
    def test_export_volume_error(self, mockServiceGetVolume, mockServiceExportVolume, mockTabular, mockPretty):
        '''
        Should not call VolumeService.export_volume when volume does not exist.

        Parameters
        ----------
        mockGetVolume (unittest.mock.MagicMock)
        mockExportVolume (unittest.mock.MagicMock)
        mockTabular (unittest.mock.MagicMock)
        mockPretty (unittest.mock.MagicMock)
        '''
        args = ["volume", "export", "-volume_id=1", "-s3_bucket_name=xvolrepo", "-s3_access_key=ABCDEFG",
            "-s3_secret_key=/52/yrwhere", "-url=https://s3.amazon.com"]

        self.callMessageFormatter(args)

        print("Testing no volume")

        try:
            self.cli.run(args)
        except SystemExit as se:
            exception = se

        assert exception != None, "Expected to get an exception but got none"

        assert mockServiceExportVolume.call_count == 0

    @patch("plugins.volume_plugin.VolumePlugin.pretty_print_volume", side_effect=mock_functions.empty_one)
    @patch("services.response_writer.ResponseWriter.writeTabularData", side_effect=mock_functions.empty_one)
    @patch("services.volume_service.VolumeService.export_volume", side_effect=mock_functions.exportVolume)
    @patch("services.volume_service.VolumeService.get_volume", side_effect=mock_functions.getVolume)
    def test_plugin_incremental(self, mockServiceGetVolume, mockServiceExportVolume, mockTabular, mockPretty):
        '''
        Command \'volume clone -from_last_export\' initiates an incremental export to a bucket.
        Indirectly tests VolumePlugin.export_volume() by observing call to volume service.

        Parameters
        ----------
        mockServiceGetVolume (unittest.mock.MagicMock)
        mockServiceExportVolume (unittest.mock.MagicMock)
        mockTabular (unittest.mock.MagicMock)
        mockPretty (unittest.mock.MagicMock)
        '''

        # Using mock in python, top level packages (like argparse) cannot be patched outright.
        # http://stackoverflow.com/questions/22750555/python-mock-patch-top-level-packages
        # TODO: Test parse_args() directly.

        print("Plugin volume export -from_last_export")

        # Crucially, there is no -from_last_export specified.
        # Expected default value for that is False.
        args = ["volume", "export", "-volume_id=3", "-s3_bucket_name=xvolrepo", "-s3_access_key=ABCDEFG",
            "-s3_secret_key=/52/yrwhere", "-url=https://s3.amazon.com"]

        self.callMessageFormatter(args)
        self.cli.run(args)

        assert mockServiceExportVolume.call_count == 1

        from_last_export = mockServiceExportVolume.call_args[0][2]
        assert from_last_export == False

        args = ["volume", "export", "-volume_id=3", "-s3_bucket_name=xvolrepo", "-s3_access_key=ABCDEFG",
            "-s3_secret_key=/52/yrwhere", "-url=https://s3.amazon.com", "-from_last_export"]

        self.callMessageFormatter(args)
        self.cli.run(args)

        assert mockServiceExportVolume.call_count == 2

        from_last_export = mockServiceExportVolume.call_args[0][2]
        assert from_last_export == True

    @patch("plugins.volume_plugin.VolumePlugin.pretty_print_volume", side_effect=mock_functions.empty_one)
    @patch("services.response_writer.ResponseWriter.writeTabularData", side_effect=mock_functions.empty_one)
    @patch("services.abstract_service.AbstractService.get_url_preamble", side_effect=mock_get_url_preamble)
    @patch("services.rest_helper.RESTHelper.post", side_effect=mock_post)
    @patch("services.volume_service.VolumeService.get_volume", side_effect=mock_functions.getVolume)
    def test_service_incremental(self, mockServiceGetVolume, mockServicePost, mockUrlPreamble, mockTabular, mockPretty):
        '''
        Command \'volume clone -from_last_export\' initiates an incremental export to a bucket.
        Directly tests the real VolumeService.export_volume

        Parameters
        ----------
        mockServiceGetVolume (unittest.mock.MagicMock)
        mockServicePost (unittest.mock.MagicMock) : Replace REST helper post() with mock empty
        mockUrlPreamble (unittest.mock.MagicMock) : Returns the string to prepend for POST Url
        mockTabular (unittest.mock.MagicMock)
        mockPretty (unittest.mock.MagicMock)
        '''
        volume = Volume();
        repo = Repository();
        repo.url = "https://s3.amazon.com"
        repo.bucket_name = "xvolrepo"
        repo.remote_om = None
        repo.credentials.access_key_id = "ABCDEFG"
        repo.credentials.secret_key = "/52/yrwhere"

        session = FdsAuth()
        service = VolumeService(session)
        service.export_volume(volume, repo, True)

        # The service export_volume is a url producer
        url = mockServicePost.call_args[0][1]
        assert mockServicePost.call_count == 1
        assert url == "http://localhost:7777/fds/config/v09/volumes/-1/exports/s3?incremental=true"

